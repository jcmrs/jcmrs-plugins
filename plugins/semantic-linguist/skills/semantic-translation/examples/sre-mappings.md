# SRE-Specific Ambiguity Resolutions

Real-world examples of ambiguous user requests mapped to precise SRE (Site Reliability Engineering) implementations.

## Overview

SRE is a discipline that applies software engineering principles to infrastructure and operations. Key concepts include:
- **Observability pillars**: Logs (events), Metrics (measurements), Traces (request paths)
- **Service levels**: SLI (indicators), SLO (objectives), SLA (agreements)
- **Incident management**: SEV levels, on-call rotations, postmortems
- **Reliability practices**: Error budgets, toil reduction, capacity planning

Common ambiguities arise when users use general terms like "observability", "SLI", "incident", "monitoring", or "on-call" without SRE-specific context.

---

## Example 1: "set up observability"

### User Request
```
"We need to set up observability for our service"
```

### Ambiguity Detected
- "observability" - which pillar(s)? (logs, metrics, traces)
- Need to clarify what aspects of system visibility are needed

### Semantic Validation Process

**Step 1: Domain Identified**
- User working on SRE/operations
- Needs system visibility

**Step 2: Query Knowledge**
- Observability has three pillars with different purposes
- Each pillar answers different questions

**Step 3: Present Options**
```
Observability consists of three pillars, each serving different needs:

1. **Logs** (discrete events)
   - What: Individual event records with details
   - When: Happened at specific timestamp
   - Tools: ELK stack, Splunk, Loki, CloudWatch Logs
   - Use case: Debugging, audit trails, error investigation
   - Example: "User X failed login at 14:23:15 due to invalid password"
   - Questions answered: What happened? When? Who? Why did it fail?

2. **Metrics** (measurements over time)
   - What: Numerical data points aggregated
   - When: Time-series data (rate, duration, count)
   - Tools: Prometheus, Grafana, Datadog, CloudWatch Metrics
   - Use case: Performance monitoring, alerting, capacity planning
   - Example: "Average response time: 234ms, Error rate: 0.3%"
   - Questions answered: How fast? How often? Trending up or down?

3. **Traces** (request journeys)
   - What: End-to-end request path through distributed system
   - When: Entire lifecycle of single request
   - Tools: Jaeger, Zipkin, AWS X-Ray, Honeycomb
   - Use case: Latency analysis, bottleneck identification, microservices debugging
   - Example: "Request spent 45ms in API, 120ms in database, 10ms in cache"
   - Questions answered: Where is the bottleneck? Which service is slow?

Which observability questions do you need to answer?"
```

**Step 4: User Clarifies**
```
User: "We're seeing slow response times and need to find where the bottleneck is"
```

**Step 5: Validated Translation**
```
"That's distributed tracing! Here's how to set it up:

**1. Instrument application for tracing:**
```python
# Example: FastAPI with OpenTelemetry tracing
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to Jaeger
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Instrument FastAPI (auto-traces HTTP requests)
FastAPIInstrumentor.instrument_app(app)

# Manual span for custom operations
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    with tracer.start_as_current_span("fetch_user") as span:
        span.set_attribute("user_id", user_id)

        # Database operation (auto-instrumented)
        user = await db.query(User).filter(User.id == user_id).first()

        # External API call (manual span)
        with tracer.start_as_current_span("fetch_profile_picture"):
            profile_url = await get_profile_from_cdn(user.profile_id)

        return {"user": user, "profile_url": profile_url}
```

**2. Deploy tracing backend (Jaeger example):**
```bash
# Docker Compose for Jaeger
version: '3'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "6831:6831/udp"  # Receive traces
      - "16686:16686"    # UI
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
```

**3. Analyze traces in Jaeger UI:**
- Access http://localhost:16686
- Search for traces with high duration
- Identify span with longest duration (bottleneck)

**Example trace breakdown:**
```
Request: GET /users/123
Total duration: 275ms

Spans:
  1. HTTP Request (275ms total)
     ├─ fetch_user (250ms)
     │  ├─ database_query (240ms) ← BOTTLENECK!
     │  └─ fetch_profile_picture (8ms)
     └─ response_serialization (2ms)
```

**Result:** Database query is bottleneck (240ms of 275ms)
**Action:** Add database index, optimize query, or cache results

**When to use each pillar:**
- Logs → "What error message did user see?"
- Metrics → "Is API getting slower over time?"
- Traces → "Where exactly is the slowdown?" (your use case)"
```

---

## Example 2: "define SLI for our service"

### User Request
```
"We need to define SLIs for our API"
```

### Ambiguity Detected
- "SLI" - which metric? (availability, latency, throughput, error rate)
- Need to clarify what reliability aspect to measure

### Semantic Validation Process

**Step 1: Explain SLI Types**
```
SLI (Service Level Indicator) is a quantitative measure of service reliability. Common SLI types:

1. **Availability SLI** (uptime percentage)
   - Measures: Successful requests / Total requests
   - Example: 99.9% of requests succeed (not 5xx errors)
   - Formula: (Total requests - Failed requests) / Total requests × 100
   - Use case: Service must be accessible

2. **Latency SLI** (response time)
   - Measures: Percentage of requests under target latency
   - Example: 95% of requests complete in < 200ms
   - Formula: (Requests < 200ms) / Total requests × 100
   - Use case: Service must be fast

3. **Throughput SLI** (capacity)
   - Measures: Requests processed per second
   - Example: Service handles ≥ 1000 requests/second
   - Formula: Total requests / Time period
   - Use case: Service must handle load

4. **Error Rate SLI** (failure percentage)
   - Measures: Failed requests / Total requests
   - Example: < 0.1% of requests return errors
   - Formula: Failed requests / Total requests × 100
   - Use case: Service must be reliable

What matters most for your API:
- Uptime → **Availability SLI**
- Speed → **Latency SLI**
- Capacity → **Throughput SLI**
- Correctness → **Error Rate SLI**"
```

**Step 2: User Clarifies**
```
User: "Our users complain when API is slow, speed matters most"
```

**Step 3: Validated Translation**
```
"That's a Latency SLI! Here's how to define and measure it:

**1. Define latency SLI with percentile:**
```yaml
# SLI Definition
Service: User API
Metric: Latency
Target: 95th percentile (p95) of requests complete in < 200ms
Measurement window: 30-day rolling window

Why p95 (not average)?
- Average hides outliers (10% slow requests = still good average)
- p95 means 95% of users have fast experience
- Captures tail latency problems
```

**2. Query metrics (Prometheus example):**
```promql
# Calculate p95 latency
histogram_quantile(
  0.95,
  rate(http_request_duration_seconds_bucket{job="user-api"}[5m])
)

# Count requests under 200ms
sum(rate(http_request_duration_seconds_bucket{
  job="user-api",
  le="0.2"  # 200ms
}[5m]))

# Calculate SLI percentage
(
  sum(rate(http_request_duration_seconds_bucket{
    job="user-api",
    le="0.2"
  }[5m]))
  /
  sum(rate(http_request_duration_seconds_count{
    job="user-api"
  }[5m]))
) * 100

# Result: 96.2% of requests < 200ms
```

**3. Define SLO (objective) from SLI:**
```yaml
# SLO (Service Level Objective)
SLI: Latency (p95 < 200ms)
Target: 95% of requests meet SLI
Measurement: 30-day rolling window
Error budget: 5% of requests can exceed 200ms

Math:
- Total requests/month: 10 million
- Error budget: 5% = 500,000 slow requests allowed
- Burn rate: How fast we consume error budget
```

**4. Alert when SLO at risk:**
```yaml
# Prometheus alert rule
groups:
  - name: slo_alerts
    rules:
      - alert: LatencySLOBreach
        expr: |
          (
            sum(rate(http_request_duration_seconds_bucket{
              job="user-api",
              le="0.2"
            }[30d]))
            /
            sum(rate(http_request_duration_seconds_count{
              job="user-api"
            }[30d]))
          ) * 100 < 95
        for: 1h
        annotations:
          summary: "Latency SLO breached - p95 latency target not met"
          description: "Only {{ $value }}% of requests under 200ms (target: 95%)"
```

**5. Track error budget:**
```python
# Error budget tracking
current_sli = 96.2  # % of requests under 200ms
slo_target = 95.0
error_budget_remaining = current_sli - slo_target  # 1.2% budget left

# With 10M requests/month:
total_requests = 10_000_000
budget_consumed = (100 - current_sli) / 100 * total_requests
# = 380,000 slow requests consumed
# = 500,000 - 380,000 = 120,000 slow requests remaining
```

**SLI vs SLO vs SLA:**
- **SLI** = Measurement (how fast service is)
- **SLO** = Internal target (95% under 200ms)
- **SLA** = Customer contract (99% uptime or refund)"
```

---

## Example 3: "we have an incident"

### User Request
```
"We have an incident, the API is down"
```

### Ambiguity Detected
- "incident" - severity level? (SEV-1 critical vs SEV-2 vs alert)
- Need to clarify impact and response urgency

### Semantic Validation Process

**Step 1: Clarify Severity**
```
SRE incidents have severity levels determining response:

1. **SEV-1 (Critical Incident)**
   - Impact: Complete outage, all users affected
   - Example: API returning 100% errors, database down, total service failure
   - Response: Immediate, page on-call, all hands on deck
   - Timeline: Acknowledge < 5 min, update every 30 min

2. **SEV-2 (Major Incident)**
   - Impact: Partial outage, significant user subset affected
   - Example: One region down, degraded performance (< 50% capacity)
   - Response: Urgent, page on-call, gather response team
   - Timeline: Acknowledge < 15 min, update every hour

3. **SEV-3 (Minor Incident)**
   - Impact: Limited impact, small user subset or non-critical feature
   - Example: Search feature slow, admin panel inaccessible
   - Response: Normal hours, create ticket, investigate next business day
   - Timeline: Acknowledge < 1 hour, resolve within SLA

4. **Alert (Not incident yet)**
   - Impact: Warning signal, potential issue, no user impact yet
   - Example: High CPU (80%), elevated error rate (0.5% vs 0.1% baseline)
   - Response: Investigate, monitor, create task if needed
   - Timeline: Review within 1 hour, escalate if degrades

What's the impact:
- All users cannot use service → **SEV-1**
- Half of users affected → **SEV-2**
- Small feature broken → **SEV-3**
- Metrics elevated but users unaffected → **Alert**"
```

**Step 2: User Clarifies**
```
User: "API is completely down, all requests return 503, all customers impacted"
```

**Step 3: Validated Translation**
```
"That's a SEV-1 Critical Incident! Here's the response protocol:

**1. Declare incident (immediately):**
```bash
# Slack incident bot or command
/incident declare
Severity: SEV-1
Title: API Complete Outage - All Requests 503
Impact: All customers unable to access service
Incident Commander: @oncall-sre

# Auto-creates:
# - Incident channel: #incident-2024-12-29-001
# - Status page update: "Investigating major outage"
# - Page on-call: SMS/phone to on-call engineer
```

**2. Assemble incident response team:**
```
Roles:
- Incident Commander (IC): @oncall-sre (coordinates response)
- Tech Lead: @backend-lead (technical investigation)
- Communications: @support-lead (customer updates)
- Scribe: @junior-sre (documents timeline)

Incident channel: #incident-2024-12-29-001
War room: Zoom link auto-generated
```

**3. Immediate actions (first 5 minutes):**
```bash
# IC: Gather information
- When started: Check monitoring alerts
- Recent changes: Check deployment history
- Current state: Verify all regions affected

# Tech Lead: Quick diagnosis
kubectl get pods -n production  # Check pod status
kubectl logs api-deployment-xyz  # Check application logs
kubectl describe pod api-xyz     # Check events

# Result: All pods crashing with "Database connection timeout"
```

**4. Mitigation (restore service):**
```bash
# Hypothesis: Recent deployment broke database connection

# Rollback deployment (fastest mitigation)
kubectl rollout undo deployment/api-deployment

# Monitor recovery
watch kubectl get pods -n production

# Verify API responding
curl https://api.example.com/health
# 200 OK - Service restored

# Elapsed time: 12 minutes from detection to recovery
```

**5. Communication timeline:**
```
[00:00] Incident detected (monitoring alert)
[00:05] SEV-1 declared, IC assigned
[00:08] Status page: "Investigating API outage affecting all users"
[00:12] Mitigation deployed (rollback)
[00:15] Status page: "Mitigation in progress, service partially restored"
[00:20] Service fully recovered
[00:25] Status page: "Incident resolved, all services operational"
[00:30] Internal update: "Root cause: deployment X broke DB connection pool config"
```

**6. Post-incident (after resolution):**
```markdown
# Incident postmortem (blameless)

## Timeline
- 14:23 UTC: Deployment 1.2.5 completed
- 14:27 UTC: First 503 errors detected
- 14:30 UTC: Monitoring alerts triggered
- 14:32 UTC: SEV-1 declared
- 14:40 UTC: Rollback initiated
- 14:44 UTC: Service restored

## Root Cause
Deployment 1.2.5 changed database connection pool config from 100 to 10 connections,
causing connection exhaustion under normal load.

## Impact
- Duration: 17 minutes complete outage
- Users affected: 100% of users (all regions)
- Requests failed: ~150,000 requests returned 503

## Action Items
- [ ] Add integration test for DB connection pool under load
- [ ] Implement gradual rollout (canary deployments)
- [ ] Add alert for connection pool exhaustion
- [ ] Review all config changes in deployment pipeline
```

**SEV-1 response checklist:**
- [ ] Incident declared within 5 minutes
- [ ] IC assigned, roles defined
- [ ] War room established
- [ ] Customer communication started (status page)
- [ ] Mitigation prioritized over root cause analysis
- [ ] Updates every 30 minutes
- [ ] Postmortem scheduled (within 48 hours)"
```

---

## Example 4: "set up monitoring"

### User Request
```
"We need to set up monitoring for our application"
```

### Ambiguity Detected
- "monitoring" - passive monitoring vs active observability vs alerting
- Need to clarify what visibility and response capability is needed

### Semantic Validation Process

**Step 1: Distinguish Monitoring Approaches**
```
"Monitoring" can mean different things in SRE:

1. **Passive Monitoring** (collect and display)
   - What: Dashboards showing metrics
   - Purpose: Visibility into system state
   - Tools: Grafana dashboards, CloudWatch dashboards
   - Use case: Engineers check dashboards reactively
   - Example: "Let me check the dashboard to see if API is healthy"
   - Limitation: Requires someone to look

2. **Active Observability** (query and investigate)
   - What: Flexible querying of logs, metrics, traces
   - Purpose: Investigate issues and understand behavior
   - Tools: Prometheus queries, Elasticsearch, Honeycomb
   - Use case: Deep-dive into specific issues
   - Example: "Why did user X see slow response at 14:23?"
   - Benefit: Answers specific questions

3. **Alerting** (automated notifications)
   - What: Automated alerts when thresholds breached
   - Purpose: Proactive notification of problems
   - Tools: Prometheus Alertmanager, PagerDuty, Opsgenie
   - Use case: Wake up on-call when service degraded
   - Example: "Alert: Error rate > 1% for 5 minutes"
   - Benefit: Don't need to watch dashboards

What's your goal:
- See current status → **Passive Monitoring**
- Investigate problems → **Active Observability**
- Get notified of problems → **Alerting**"
```

**Step 2: User Clarifies**
```
User: "We want to be notified automatically when something goes wrong, not manually check"
```

**Step 3: Validated Translation**
```
"That's Alerting! Here's how to set it up properly:

**1. Define alert conditions (Prometheus example):**
```yaml
# prometheus-alerts.yml
groups:
  - name: api_alerts
    rules:
      # High error rate alert
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) * 100 > 1
        for: 5m  # Must be true for 5 minutes (avoid flapping)
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High API error rate detected"
          description: "Error rate is {{ $value }}% (threshold: 1%)"

      # High latency alert
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 0.5
        for: 10m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "API latency exceeds threshold"
          description: "p95 latency is {{ $value }}s (threshold: 0.5s)"

      # Service down alert
      - alert: ServiceDown
        expr: up{job="api"} == 0
        for: 1m
        labels:
          severity: critical
          team: sre
        annotations:
          summary: "API service is down"
          description: "API has been unavailable for 1 minute"
```

**2. Configure Alertmanager (routing and notifications):**
```yaml
# alertmanager.yml
global:
  slack_api_url: 'https://hooks.slack.com/services/XXX'
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

route:
  receiver: 'team-default'
  group_by: ['alertname', 'cluster']
  group_wait: 30s      # Wait to batch alerts
  group_interval: 5m   # Re-send interval
  repeat_interval: 4h  # Re-send if still firing

  routes:
    # Critical alerts → PagerDuty (page on-call)
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true  # Also send to Slack

    # Critical alerts → Slack
    - match:
        severity: critical
      receiver: 'slack-critical'

    # Warning alerts → Slack only (no page)
    - match:
        severity: warning
      receiver: 'slack-warnings'

receivers:
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ .GroupLabels.alertname }}: {{ .CommonAnnotations.summary }}'

  - name: 'slack-critical'
    slack_configs:
      - channel: '#alerts-critical'
        title: '🚨 {{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.description }}'

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#alerts-warnings'
        title: '⚠️ {{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.description }}'
```

**3. Define on-call rotation (PagerDuty example):**
```
Schedule: "Backend SRE On-Call"
Rotation:
  - Week 1: Alice (primary), Bob (backup)
  - Week 2: Bob (primary), Charlie (backup)
  - Week 3: Charlie (primary), Alice (backup)

Escalation policy:
  1. Page primary on-call → Wait 5 minutes
  2. If no ACK → Page backup on-call → Wait 5 minutes
  3. If no ACK → Page SRE manager

Contact methods:
  - Push notification
  - SMS
  - Phone call
```

**4. Alert best practices:**

**Good alert (actionable):**
```yaml
- alert: HighDatabaseConnections
  expr: db_connections > 90
  annotations:
    summary: "Database connection pool near exhaustion"
    description: "{{ $value }} connections used (max: 100)"
    runbook: "https://wiki.company.com/runbooks/db-connections"
    dashboard: "https://grafana.company.com/d/db-overview"
```

**Bad alert (not actionable):**
```yaml
- alert: CPUHigh
  expr: cpu_usage > 50
  # Problem: 50% is not necessarily bad, no context
```

**Alert severity guidelines:**
- **Critical** = User-facing impact, immediate response, page on-call
- **Warning** = Potential issue, investigate during business hours, Slack notification
- **Info** = Logging/metrics, no notification

**Avoid alert fatigue:**
- Set thresholds based on SLO impact, not arbitrary numbers
- Use `for:` duration to avoid flapping (require sustained condition)
- Aggregate similar alerts (don't alert per pod, alert per service)
- Include runbook links for common issues"
```

---

## Example 5: "on-call rotation"

### User Request
```
"How should we handle on-call for our team?"
```

### Ambiguity Detected
- "on-call" - rotation schedule vs on-call responsibilities vs escalation
- Need to clarify on-call structure

### Semantic Validation Process

**Step 1: Explain On-Call Components**
```
On-call systems have three components:

1. **On-Call Rotation** (who is on-call when)
   - Primary on-call: First responder for incidents
   - Backup on-call: Escalation if primary unavailable
   - Rotation frequency: Weekly, bi-weekly, monthly
   - Example: Alice (primary week 1), Bob (primary week 2)

2. **On-Call Responsibilities** (what on-call engineer does)
   - Respond to alerts/pages within SLA (e.g., 15 minutes)
   - Triage incidents, determine severity
   - Mitigate issues or escalate to specialists
   - Document incident timeline
   - Example: "On-call ACKs alert, investigates, rolls back bad deployment"

3. **Escalation Policy** (when to escalate)
   - Level 1: Primary on-call
   - Level 2: Backup on-call (if primary doesn't ACK in X minutes)
   - Level 3: Manager/Tech Lead
   - Level 4: Engineering Director
   - Example: "Primary doesn't ACK in 5 min → page backup"

Which aspect are you setting up?"
```

**Step 2: User Clarifies**
```
User: "Need to set up the rotation schedule and define responsibilities"
```

**Step 3: Validated Translation**
```
"Here's a complete on-call setup:

**1. Define rotation schedule:**
```yaml
# On-Call Rotation (PagerDuty format)
Team: Backend SRE
Schedule Name: Backend Primary On-Call

Rotation Type: Weekly
Handoff Time: Monday 9:00 AM PST
Participants:
  - Alice (alice@company.com)
  - Bob (bob@company.com)
  - Charlie (charlie@company.com)

Schedule:
  - Week of Dec 30: Alice (primary), Bob (backup)
  - Week of Jan 6:  Bob (primary), Charlie (backup)
  - Week of Jan 13: Charlie (primary), Alice (backup)
  - (repeats)

Backup rotation: Same schedule, shifted one week
```

**2. Define on-call responsibilities:**
```markdown
# On-Call Playbook

## Response SLAs
- **Critical alerts (SEV-1)**: Acknowledge within 5 minutes, join war room
- **Major alerts (SEV-2)**: Acknowledge within 15 minutes, investigate
- **Warning alerts**: Acknowledge within 1 hour, create ticket

## Primary Responsibilities
1. **Alert Response**
   - Acknowledge alerts in PagerDuty within SLA
   - Triage: Determine severity (SEV-1/2/3 or false alarm)
   - Investigate using runbooks and monitoring tools

2. **Incident Management**
   - SEV-1: Immediately escalate to IC, join war room
   - SEV-2: Form response team, coordinate mitigation
   - SEV-3: Create ticket, investigate during business hours

3. **Communication**
   - Update incident channel every 30 minutes (SEV-1)
   - Update status page if customer-facing impact
   - Notify backup on-call if need assistance

4. **Documentation**
   - Log incident timeline in incident management tool
   - Document mitigation steps taken
   - Create postmortem action items

## Escalation Scenarios
Escalate to backup on-call when:
- Issue outside your domain expertise (e.g., database specialist needed)
- Need additional hands for investigation
- Incident duration > 1 hour without resolution

Escalate to manager when:
- Customer escalation or high-profile incident
- Need architecture decision
- Cross-team coordination required
```

**3. Create runbooks for common issues:**
```markdown
# Runbook: High Error Rate Alert

## Symptoms
- Alert: "HighErrorRate" firing
- API returning 5xx errors > 1% of requests

## Investigation Steps
1. Check recent deployments
   \`\`\`bash
   kubectl rollout history deployment/api
   # Note: Last deployment 10 minutes ago
   \`\`\`

2. Check application logs
   \`\`\`bash
   kubectl logs -l app=api --tail=100 | grep ERROR
   # Look for: Database errors, timeout errors, auth failures
   \`\`\`

3. Check dependencies
   - Database: Check database dashboard (link)
   - Cache: Check Redis dashboard (link)
   - External APIs: Check status pages

## Mitigation
### If recent deployment:
\`\`\`bash
kubectl rollout undo deployment/api
# Wait 2 minutes, verify error rate drops
\`\`\`

### If database issue:
\`\`\`bash
# Check connection pool
kubectl exec -it api-pod -- curl localhost:8080/debug/db-pool
# If exhausted, scale replicas:
kubectl scale deployment/api --replicas=10
\`\`\`

### If external API issue:
- Enable circuit breaker in config
- Switch to fallback provider (see docs/failover.md)

## Escalation
- If mitigation doesn't work in 15 minutes → Escalate to Tech Lead
- If database issue → Escalate to Database team (#team-database)
```

**4. On-call best practices:**

**Handoff ritual (Monday 9am):**
```
Previous on-call to new on-call:
1. Review incidents from past week
2. Share known issues or ongoing investigations
3. Highlight upcoming deployments or maintenance
4. Confirm contact info and PagerDuty setup working

Slack: #oncall-handoff
Template:
  - Week: Dec 23-29
  - Incidents: 2 SEV-2, 5 SEV-3
  - Ongoing: Database migration scheduled for Wednesday
  - Notes: Redis cluster showing intermittent latency spikes
```

**On-call compensation:**
- On-call stipend: $X per week
- Incident response credit: Y hours time-off per incident
- Goal: Max 2-3 alerts per week (reduce toil if higher)

**Improve on-call experience:**
- Write runbooks for repeat incidents
- Automate mitigation where possible (auto-scaling, auto-restart)
- Post-incident reviews to prevent recurrence
- Toil reduction sprints to fix chronic issues"
```

---

## Pattern Summary

Common SRE ambiguity patterns:

1. **"observability"** → Logs (events) vs Metrics (measurements) vs Traces (request paths) - three pillars
2. **"SLI"** → Availability (uptime %) vs Latency (p95 response time) vs Throughput (requests/sec) vs Error Rate (% failures)
3. **"incident"** → SEV-1 (critical, all users) vs SEV-2 (major, subset) vs SEV-3 (minor) vs Alert (warning, no user impact)
4. **"monitoring"** → Passive monitoring (dashboards) vs Active observability (queries) vs Alerting (notifications)
5. **"on-call"** → Rotation schedule vs Responsibilities (what on-call does) vs Escalation policy

**Key distinctions:**
- **Observability pillars** answer different questions (what? how fast? where?)
- **SLI types** measure different reliability aspects (speed, uptime, capacity, correctness)
- **Incident severity** drives response urgency and communication frequency
- **Monitoring types** differ in proactivity (passive watching vs automated alerts)
- **On-call components** cover schedule, duties, and escalation paths

Always clarify which observability pillar, SLI metric, incident severity, monitoring approach, or on-call aspect before implementing SRE practices!
