# FastAPI-Specific Ambiguity Resolutions

Real-world examples of ambiguous user requests mapped to precise FastAPI implementations.

## Overview

FastAPI is a modern Python web framework for building APIs with automatic validation, serialization, and interactive documentation. Key concepts include:
- **Path operations**: Endpoint decorators (@app.get, @app.post, @app.put, @app.delete)
- **Dependency injection**: Depends() system for reusable components
- **Pydantic models**: Request/response validation and serialization
- **APIRouter**: Endpoint organization and modular structure

Common ambiguities arise when users use general terms like "dependency", "endpoint", "model", "route", or "validation" without FastAPI-specific context.

---

## Example 1: "add dependencies to my api"

### User Request
```
"I need to add dependencies to my FastAPI application"
```

### Ambiguity Detected
- "dependencies" - could mean FastAPI Depends(), pip packages, or architectural dependencies
- Need to clarify which type of dependency

### Semantic Validation Process

**Step 1: Domain Identified**
- User working with FastAPI
- "dependencies" has multiple meanings in this context

**Step 2: Query Knowledge**
- FastAPI Depends() for dependency injection
- pip dependencies for external packages
- Architectural dependencies between services

**Step 3: Present Options**
```
In FastAPI context, "dependencies" can mean:

1. **FastAPI Dependency Injection (Depends())**
   - Reusable components injected into path operations
   - Example: Authentication, database sessions, configuration
   - Declared with: Depends(dependency_function)
   - Use case: Share logic across endpoints (auth, DB access)

2. **Pip Package Dependencies**
   - External Python libraries your app uses
   - Declared in: requirements.txt or pyproject.toml
   - Example: fastapi, uvicorn, sqlalchemy, pydantic
   - Use case: Add third-party functionality

3. **Architectural Service Dependencies**
   - External services your API depends on
   - Example: Database, Redis, message queue, external APIs
   - Configured via: Environment variables, settings
   - Use case: System integration and infrastructure

Which type of dependency do you need?"
```

**Step 4: User Clarifies**
```
User: "I want to add authentication that's reused across multiple endpoints"
```

**Step 5: Validated Translation**
```
"That's FastAPI Dependency Injection with Depends()! Here's the pattern:

**1. Define dependency function:**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency that validates JWT token and returns current user.
    Injected into endpoints that require authentication.
    """
    token = credentials.credentials

    # Validate token (your logic)
    user = validate_jwt_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    return user
```

**2. Inject into path operations:**
```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/protected")
async def protected_route(
    current_user: dict = Depends(get_current_user)  # Dependency injection
):
    """
    FastAPI automatically:
    1. Calls get_current_user() before running this function
    2. Passes result as current_user parameter
    3. Returns 401 if dependency raises HTTPException
    """
    return {"message": f"Hello {current_user['name']}", "user": current_user}

@app.get("/admin")
async def admin_route(
    current_user: dict = Depends(get_current_user)  # Reused dependency
):
    """Same dependency, different endpoint - DRY principle"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return {"message": "Admin access granted"}
```

**3. Chain dependencies:**
```python
async def get_db():
    """Dependency that provides database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_active_user(
    current_user: dict = Depends(get_current_user),  # Depends on auth
    db: Session = Depends(get_db)  # Depends on database
):
    """Chained dependency - uses both auth and database"""
    user_from_db = db.query(User).filter(User.id == current_user["id"]).first()
    if not user_from_db.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user_from_db
```

**Benefits of FastAPI Depends():**
- Declare once, reuse everywhere
- Automatic execution before endpoint
- Dependency chaining for complex logic
- Type hints for IDE autocomplete
- Automatic OpenAPI documentation"
```

---

## Example 2: "create an endpoint"

### User Request
```
"I need to create an endpoint for user registration"
```

### Ambiguity Detected
- "endpoint" - could mean FastAPI path operation or external API endpoint
- Need to clarify if they're creating or calling an endpoint

### Semantic Validation Process

**Step 1: Analyze Context**
```
"Endpoint" in FastAPI context could mean:

1. **FastAPI Path Operation** (creating an endpoint)
   - HTTP endpoint your API exposes
   - Defined with: @app.post("/users"), @app.get("/users/{id}")
   - Example: POST /api/users for user registration
   - Use case: Building your API's functionality

2. **External API Endpoint** (calling an endpoint)
   - Third-party API your code calls
   - Used with: httpx, requests library
   - Example: Calling auth0.com/api/users
   - Use case: Integrating external services

Are you creating an endpoint (for others to call your API) or calling an endpoint (integrating external API)?"
```

**Step 2: User Clarifies**
```
User: "Creating an endpoint - users will POST registration data to my API"
```

**Step 3: Validated Translation**
```
"That's a FastAPI path operation! Here's how to create it:

**1. Define Pydantic model for request validation:**
```python
from pydantic import BaseModel, EmailStr, Field

class UserRegistration(BaseModel):
    """Request model for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # Validates email format
    password: str = Field(..., min_length=8)
    full_name: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "securepass123",
                "full_name": "John Doe"
            }
        }

class UserResponse(BaseModel):
    """Response model (excludes sensitive fields)"""
    id: int
    username: str
    email: EmailStr
    full_name: str | None

    class Config:
        from_attributes = True  # Allow ORM model conversion
```

**2. Create path operation:**
```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.post(
    "/api/users",  # Endpoint path
    response_model=UserResponse,  # Response validation
    status_code=status.HTTP_201_CREATED,  # Success status
    tags=["users"],  # OpenAPI grouping
    summary="Register new user"  # OpenAPI summary
)
async def register_user(user_data: UserRegistration):
    """
    Register a new user account.

    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Secure password (minimum 8 characters)
    - **full_name**: Optional full name

    Returns the created user (without password).
    """

    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Create user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user  # Automatically serialized to UserResponse
```

**3. What FastAPI does automatically:**
- Validates request body against UserRegistration model
- Returns 422 if validation fails (with detailed errors)
- Serializes response to UserResponse model
- Generates OpenAPI documentation
- Creates interactive docs at /docs"
```

---

## Example 3: "use models in fastapi"

### User Request
```
"How do I use models in FastAPI?"
```

### Ambiguity Detected
- "models" - could mean Pydantic models, database models, or ML models
- Need to clarify which type of model

### Semantic Validation Process

**Step 1: Present Options**
```
"Models" in FastAPI applications can mean:

1. **Pydantic Models** (request/response validation)
   - Define API data structures
   - Automatic validation and serialization
   - Example: UserCreate, UserResponse models
   - Use case: API contracts, input validation

2. **Database ORM Models** (SQLAlchemy/Tortoise)
   - Define database tables
   - ORM mapping to database
   - Example: User table model with columns
   - Use case: Database operations, persistence

3. **Machine Learning Models** (scikit-learn, PyTorch)
   - Trained ML models for predictions
   - Loaded and used in endpoints
   - Example: Sentiment analysis model
   - Use case: AI/ML inference in API

Which type of model are you asking about?"
```

**Step 2: User Clarifies**
```
User: "I want to validate incoming request data"
```

**Step 3: Validated Translation**
```
"That's Pydantic models for request validation! Here's the complete pattern:

**1. Define Pydantic models:**
```python
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    """Pydantic model for creating products"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)  # Greater than 0
    category: str
    tags: List[str] = []

    @validator('price')
    def validate_price(cls, v):
        """Custom validation: price must be reasonable"""
        if v > 100000:
            raise ValueError('Price seems unreasonably high')
        return round(v, 2)  # Round to 2 decimals

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 999.99,
                "category": "electronics",
                "tags": ["tech", "portable"]
            }
        }

class ProductResponse(BaseModel):
    """Pydantic model for product responses"""
    id: int
    name: str
    description: Optional[str]
    price: float
    category: str
    tags: List[str]
    created_at: datetime

    class Config:
        from_attributes = True  # Allow SQLAlchemy model conversion

class ProductUpdate(BaseModel):
    """Pydantic model for updating products (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    tags: Optional[List[str]] = None
```

**2. Use in path operations:**
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    """
    FastAPI automatically:
    - Validates product data against ProductCreate schema
    - Returns 422 with validation errors if invalid
    - Parses JSON body into ProductCreate object
    """

    # product.name, product.price, etc. are already validated
    db_product = Product(**product.dict())  # Convert Pydantic → ORM model
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product  # Converted to ProductResponse automatically

@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, updates: ProductUpdate):
    """
    Partial updates - only provided fields are validated
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update only provided fields
    update_data = updates.dict(exclude_unset=True)  # Only set fields
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product
```

**3. Relationship between Pydantic and ORM models:**
```python
# Database ORM model (SQLAlchemy)
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    """Database table definition"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

# Workflow:
# Request JSON → Pydantic ProductCreate → Validation → ORM Product → Database
# Database → ORM Product → Pydantic ProductResponse → Response JSON

**Key distinction:**
- **Pydantic models** = API layer (validation, serialization, documentation)
- **ORM models** = Database layer (persistence, queries, relationships)
- Convert between them as needed"
```

---

## Example 4: "add routes to fastapi"

### User Request
```
"How do I organize routes in FastAPI?"
```

### Ambiguity Detected
- "routes" - could mean individual path operations or APIRouter for organization
- Need to clarify organization strategy

### Semantic Validation Process

**Step 1: Explain Options**
```
FastAPI route organization has two levels:

1. **Path Operations** (individual routes)
   - Single endpoint definitions
   - Example: @app.get("/users"), @app.post("/products")
   - Use for: Simple apps with few endpoints
   - Pattern: All routes in main file

2. **APIRouter** (route grouping)
   - Group related endpoints together
   - Example: UserRouter, ProductRouter, AuthRouter
   - Use for: Larger apps, modular structure
   - Pattern: Separate router modules, imported into main

Your app has 50+ endpoints across users, products, orders, and auth. Which organization would help?"
```

**Step 2: User Clarifies**
```
User: "I have many endpoints, want to organize by feature area"
```

**Step 3: Validated Translation**
```
"That's APIRouter for modular organization! Here's the structure:

**1. Create feature routers (routers/users.py):**
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List

# Create router instance
router = APIRouter(
    prefix="/users",  # All routes prefixed with /users
    tags=["users"],   # OpenAPI grouping
    dependencies=[Depends(verify_api_key)]  # Applied to all routes
)

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all users - becomes GET /users/"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Create user - becomes POST /users/"""
    # ... creation logic
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID - becomes GET /users/{user_id}"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**2. Create more routers (routers/products.py, routers/auth.py):**
```python
# routers/products.py
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
async def list_products():
    """GET /products/"""
    pass

@router.post("/")
async def create_product(product: ProductCreate):
    """POST /products/"""
    pass

# routers/auth.py
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
async def login(credentials: LoginCredentials):
    """POST /auth/login"""
    pass

@router.post("/refresh")
async def refresh_token(token: str):
    """POST /auth/refresh"""
    pass
```

**3. Include routers in main app:**
```python
from fastapi import FastAPI
from routers import users, products, auth

app = FastAPI(title="My API", version="1.0.0")

# Include all routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)

# Can also add prefix at include time
app.include_router(
    admin.router,
    prefix="/api/v1",  # Adds /api/v1 before router's prefix
    tags=["admin"]
)

# Result:
# GET /users/ → users.list_users
# POST /users/ → users.create_user
# GET /products/ → products.list_products
# POST /auth/login → auth.login
# GET /api/v1/admin/dashboard → admin.dashboard
```

**4. Project structure:**
```
my_api/
├── main.py             # App instance, router inclusion
├── routers/
│   ├── __init__.py
│   ├── users.py        # User endpoints
│   ├── products.py     # Product endpoints
│   ├── auth.py         # Auth endpoints
│   └── admin.py        # Admin endpoints
├── models/
│   ├── schemas.py      # Pydantic models
│   └── database.py     # ORM models
└── dependencies.py     # Shared dependencies (auth, db)
```

**Benefits of APIRouter:**
- Logical grouping by feature/domain
- Separate files for maintainability
- Reusable dependencies per router
- Clear OpenAPI organization (tags)
- Team can work on different routers simultaneously"
```

---

## Example 5: "add validation to api"

### User Request
```
"I need to add validation to my FastAPI endpoints"
```

### Ambiguity Detected
- "validation" - could mean Pydantic automatic validation or custom business logic validation
- Need to clarify validation type

### Semantic Validation Process

**Step 1: Clarify Scope**
```
FastAPI supports two types of validation:

1. **Pydantic Automatic Validation**
   - Type checking, format validation, constraints
   - Happens automatically via Pydantic models
   - Example: Email format, min/max length, numeric ranges
   - Built-in, no custom code needed

2. **Custom Business Logic Validation**
   - Domain-specific rules
   - Implemented via Pydantic validators or endpoint logic
   - Example: "Username must be unique", "Order total matches items"
   - Requires custom implementation

Which type of validation do you need?"
```

**Step 2: User Clarifies**
```
User: "Both - I need basic validation and also business rules"
```

**Step 3: Validated Translation**
```
"FastAPI supports both through Pydantic! Here's how:

**1. Pydantic automatic validation (built-in):**
```python
from pydantic import BaseModel, Field, EmailStr, constr, validator
from typing import List
from datetime import date

class UserCreate(BaseModel):
    # Type validation (automatic)
    username: str  # Must be string
    age: int  # Must be integer

    # Format validation (automatic)
    email: EmailStr  # Must be valid email format

    # Constraint validation (automatic)
    password: constr(min_length=8, max_length=100)  # Length constraints
    bio: str = Field(None, max_length=500)  # Field-level constraints
    age: int = Field(..., ge=18, le=120)  # Greater/less than constraints

    # Enum validation (automatic)
    role: Literal["user", "admin", "moderator"]  # Must be one of these

# FastAPI automatically validates and returns 422 with errors if validation fails
```

**2. Custom business logic validation (Pydantic validators):**
```python
from pydantic import BaseModel, validator, root_validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str
    birth_date: date

    @validator('username')
    def username_alphanumeric(cls, v):
        """Custom validation: username must be alphanumeric"""
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    @validator('password')
    def password_strength(cls, v):
        """Custom validation: password requirements"""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @validator('birth_date')
    def validate_age(cls, v):
        """Custom validation: user must be 18+"""
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError('Must be at least 18 years old')
        return v

    @root_validator
    def passwords_match(cls, values):
        """Cross-field validation: passwords must match"""
        password = values.get('password')
        password_confirm = values.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValueError('Passwords do not match')

        return values
```

**3. Endpoint-level validation (database checks):**
```python
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,  # Pydantic validation happens first
    db: Session = Depends(get_db)
):
    """
    Validation flow:
    1. Pydantic validates request body (automatic)
    2. Custom validators run (username, password, age)
    3. Endpoint checks database constraints (below)
    """

    # Database-level validation: check uniqueness
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

    # Business logic validation: check banned domains
    email_domain = user_data.email.split('@')[1]
    banned_domains = ["tempmail.com", "throwaway.email"]

    if email_domain in banned_domains:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email domain not allowed"
        )

    # All validation passed, create user
    new_user = User(**user_data.dict(exclude={'password_confirm'}))
    db.add(new_user)
    db.commit()

    return new_user
```

**Validation order:**
1. **Pydantic automatic** - Types, formats, constraints (422 error if fails)
2. **Custom validators** - Business rules (@validator, @root_validator) (422 error)
3. **Endpoint logic** - Database checks, external validations (400/409 error)

**When to use each:**
- **Automatic**: Data format, types, ranges
- **Validators**: Reusable business rules, cross-field checks
- **Endpoint logic**: Database constraints, external API checks, complex workflows"
```

---

## Pattern Summary

Common FastAPI ambiguity patterns:

1. **"dependency"** → FastAPI Depends() (injection) vs pip dependency (package) vs architectural dependency (service)
2. **"endpoint"** → Path operation (@app.get) vs external API endpoint (calling third-party)
3. **"model"** → Pydantic model (validation) vs ORM model (database) vs ML model (inference)
4. **"route"** → Individual path operation vs APIRouter (grouping) vs URL routing concept
5. **"validation"** → Pydantic automatic (format/type) vs custom validators (business logic) vs endpoint checks (database)

**Key distinctions:**
- **Depends()** for shared logic (auth, DB sessions), **not** pip packages
- **Path operations** create endpoints, **httpx/requests** call external endpoints
- **Pydantic models** for API layer, **ORM models** for database layer
- **APIRouter** for organization, **path operations** for individual routes
- **Pydantic validators** run before endpoint, **endpoint logic** runs after validation

Always clarify FastAPI-specific context before implementing!
