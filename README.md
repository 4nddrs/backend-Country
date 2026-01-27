# 🐴 Country Club ERP - Backend API

A comprehensive **FastAPI** backend system designed for equestrian facility management. This API provides complete control over horse care, employee management, inventory tracking, veterinary procedures, financial operations, and automated notifications via Telegram.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Core Modules](#-core-modules)
- [Telegram Integration](#-telegram-integration)
- [Automated Scheduler](#-automated-scheduler)
- [Dashboard & Analytics](#-dashboard--analytics)
- [API Usage Examples](#-api-usage-examples)
- [Development Guidelines](#-development-guidelines)

---

## 🎯 Features

### Core Management Systems

- **🐴 Horse Management**: Complete horse registry with photos, health records, nutritional plans, and owner assignments
- **👨‍🌾 Employee Management**: Staff administration with positions, contracts, salaries, absences, and shift scheduling
- **👔 Owner Management**: Owner profiles with payment tracking and monthly reports
- **💊 Medicine Inventory**: Advanced medication tracking with expiration alerts and stock monitoring
- **🌾 Food Stock Control**: Feed inventory management with supplier tracking and alpha control
- **💰 Financial Operations**: Complete income and expense tracking with monthly analytics

### Advanced Features

- **📊 Real-time Dashboard**: Comprehensive analytics with cached data for optimal performance
- **🤖 Telegram Bot Integration**: Automated notifications for veterinarians about medication alerts
- **⏰ Automated Scheduler**: Daily medication checks with smart notification system
- **📅 Vaccination Plans**: Scheduled vaccination programs with dose tracking
- **🩺 Horse Care Procedures**: Medical procedures scheduling and application tracking
- **📈 Monthly Owner Reports**: Automated billing with detailed consumption reports
- **👥 Employee Shifts**: Complete shift management system with employee assignments
- **🔐 User Authentication**: Role-based access control with Supabase Auth
- **📄 Pagination Support**: Built-in pagination utilities for all list endpoints

---

## 🏗️ Architecture

This API follows a **clean architecture** pattern with clear separation of concerns:

```
┌─────────────────┐
│   FastAPI App   │
└────────┬────────┘
         │
    ┌────┴────────────────────────┐
    │                             │
┌───▼────┐                  ┌─────▼──────┐
│Routers │◄────────────────►│  Schemas   │
└───┬────┘                  └────────────┘
    │
┌───▼────┐                  ┌────────────┐
│  CRUD  │◄────────────────►│  Supabase  │
└───┬────┘                  └────────────┘
    │
┌───▼────────┐
│  Services  │
└────────────┘
```

- **Routers**: Handle HTTP requests and responses
- **Schemas**: Pydantic models for data validation
- **CRUD**: Database operations layer
- **Services**: Business logic and external integrations
- **Utils**: Shared utilities (pagination, helpers)

---

## 📂 Project Structure

```bash
backend-Country/
├── app/
│   ├── main.py                    # Application entry point
│   ├── config.py                  # Environment configuration
│   ├── supabase_client.py         # Supabase connection manager
│   ├── scheduler.py               # APScheduler for automated tasks
│   │
│   ├── crud/                      # Database operations (25+ modules)
│   │   ├── employee.py
│   │   ├── horse.py
│   │   ├── medicine.py
│   │   ├── vaccination_plan.py
│   │   └── ...
│   │
│   ├── routers/                   # API endpoints (28+ routers)
│   │   ├── employee.py
│   │   ├── horse.py
│   │   ├── medicine.py
│   │   ├── dashboard.py           # Analytics endpoint
│   │   ├── telegram.py            # Telegram bot webhook
│   │   └── ...
│   │
│   ├── schemas/                   # Pydantic models (25+ schemas)
│   │   ├── employee.py
│   │   ├── horse.py
│   │   ├── medicine.py
│   │   └── ...
│   │
│   ├── scripts/
│   │   └── notifier.py            # Telegram notification helper
│   │
│   ├── services/                  # Business logic layer
│   │
│   └── utils/
│       └── pagination.py          # Pagination utilities
│
├── requirements.txt               # Python dependencies
├── dataSchema.sql                 # Database schema reference
└── README.md                      # This file
```

---

## ⚙️ Requirements

- **Python**: 3.10 or newer
- **pip**: Package installer for Python
- **Supabase Account**: For database and authentication
- **Telegram Bot** (optional): For automated notifications
- **Virtual Environment** (recommended)

### Key Dependencies

- `fastapi==0.116.1` - Modern web framework
- `uvicorn==0.35.0` - ASGI server
- `supabase==2.18.1` - Database client
- `pydantic==2.11.7` - Data validation
- `APScheduler==3.10.4` - Task scheduler
- `pyTelegramBotAPI==4.29.1` - Telegram bot integration

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend-Country
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (optional, as values are in `config.py`):

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
TELEGRAM_BOT_TOKEN=your-bot-token
```

### Telegram Bot Setup

1. Create a bot with [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Update the `TELEGRAM_BOT_TOKEN` in `config.py` or `.env`
4. Set your webhook URL in `main.py` (line 69)

### Supabase Configuration

1. Create a Supabase project
2. Import the schema from `dataSchema.sql` (for reference)
3. Update connection details in `config.py`

---

## 🚀 Running the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📚 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Available Endpoints (28+ routers)

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **Horses** | `/horses` | CRUD operations + filter by owner |
| **Employees** | `/employees` | Staff management + positions |
| **Owners** | `/owners` | Owner profiles and reports |
| **Medicine** | `/medicines` | Inventory with expiration tracking |
| **Food Stock** | `/food_stock` | Feed inventory management |
| **Food Providers** | `/food_provider` | Supplier information |
| **Vaccination Plans** | `/vaccination_plan` | Vaccine schedules |
| **Vaccination Applications** | `/vaccination_plan_application` | Vaccine administration records |
| **Scheduled Procedures** | `/scheduled_procedure` | Annual procedure planning |
| **Application Procedures** | `/application_procedure` | Procedure execution logs |
| **Attention Horse** | `/attention_horse` | Medical attention records |
| **Nutritional Plans** | `/nutritional_plan` | Diet planning |
| **Nutritional Details** | `/nutritional_plan_details` | Diet specifications |
| **Alpha Control** | `/alpha_control` | Alpha feed purchase tracking |
| **Tasks** | `/task` | Task management |
| **Task Categories** | `/task_category` | Task classification |
| **Employee Absences** | `/employee_absence` | Vacation & absence tracking |
| **Shifts** | `/shift_type`, `/shift_employed` | Shift management |
| **Employee Shifts** | `/employees_shiftem` | Shift assignments |
| **Expenses** | `/expenses` | Expense tracking |
| **Income** | `/income` | Income tracking |
| **Salary Payments** | `/salary_payment` | Employee salary records |
| **Tip Payments** | `/tip_payment` | Employee tip tracking |
| **Owner Reports** | `/owner_report_month` | Monthly billing reports |
| **Horse Assignments** | `/horse_assignment` | Employee-horse assignments |
| **Total Control** | `/total_control` | Complete horse cost calculations |
| **Races** | `/race` | Horse breed management |
| **User Roles** | `/user_role` | Role management |
| **ERP Users** | `/erp_user` | User account management |
| **Dashboard** | `/dashboard` | Analytics & statistics |
| **Telegram** | `/telegram/webhook` | Bot webhook endpoint |

---

## 🔧 Core Modules

### 1. Horse Management

Complete horse lifecycle management with:
- Basic information (name, photo, birthdate, sex, color)
- Passport numbers and identification
- Location tracking (box, section, basket)
- State management (ACTIVO/INACTIVO)
- School status tracking
- Owner assignments
- Nutritional plan associations
- Race/breed information

**Endpoints:**
- `GET /horses` - List all horses with pagination
- `POST /horses` - Register new horse
- `GET /horses/{id}` - Get horse details
- `PUT /horses/{id}` - Update horse information
- `DELETE /horses/{id}` - Remove horse
- `GET /horses/by_owner/{id}` - Filter horses by owner

### 2. Employee Management

Comprehensive HR system featuring:
- Personal information and photos
- Contract dates (start/end)
- Working hours (entry/exit time)
- Salary management
- Position assignments
- Active status tracking
- User account linking (UID)

**Related Modules:**
- **Employee Positions**: Job role definitions
- **Employee Absences**: Vacation and absence tracking
- **Shift Management**: Work schedule organization
- **Salary Payments**: Payment tracking with status
- **Tip Payments**: Additional compensation records

### 3. Medicine Inventory System

Advanced medication tracking with:
- Stock level monitoring (current/minimum)
- Expiration date tracking (box + opened dates)
- Days after opening calculations
- Automatic expiration status updates
- Stock status indicators
- Notification days configuration
- Source tracking (general/horse-specific)
- Active/inactive status

**Smart Features:**
- Automatic expiration calculation
- Low stock detection
- Telegram notifications for alerts
- Horse-specific medication tracking

### 4. Vaccination Management

Comprehensive immunization system:
- **Vaccination Plans**: Annual schedules with monthly doses
- **Plan Applications**: Execution records with observations
- Medicine association
- Alert status monitoring
- Employee tracking for administrations
- Horse-specific vaccination history

### 5. Nutritional Management

Complete feed planning system:
- **Nutritional Plans**: Diet programs with date ranges
- **Plan Details**: Food consumption per item
- Daily and monthly consumption tracking
- Period-based planning
- Horse assignment integration
- Food stock deduction

### 6. Financial Management

Full accounting system:
- **Income Tracking**: Revenue recording with descriptions
- **Expense Tracking**: Cost management with categories
- **Owner Reports**: Monthly billing with itemized charges
- **Alpha Control**: Feed purchase and sales tracking
- **Total Control**: Complete cost calculations per horse

**Billing Items:**
- Box/section/basket fees
- Alpha consumption
- Chala (feed) costs
- Veterinary services
- Vaccine applications
- Deworming
- Anemia exams
- External trainers
- Fines and other charges

### 7. Task Management

Work organization system:
- Task creation with categories
- Employee assignments
- Status tracking (pending/in-progress/completed)
- Completion date monitoring
- Category-based organization

### 8. Procedural Management

Medical procedure scheduling:
- **Scheduled Procedures**: Annual planning with monthly schedules
- **Application Procedures**: Execution tracking
- Alert label system
- Horse-specific procedure history
- Observation recording

---

## 🤖 Telegram Integration

### Bot Commands

- `/start` - Initialize bot and link veterinarian account
- `/help` - Show available commands

### Interactive Menu

The bot provides three main options:
1. **View All Medications** - Complete inventory list
2. **Low/Out of Stock** - Critical stock alerts
3. **Expiring/Expired** - Expiration warnings

### Notification System

Automated alerts for:
- **Low Stock**: When medication reaches or falls below minimum stock
- **Expiration Warnings**: Configurable days before expiration
- **Critical Alerts**: Immediate notifications for critical situations

### Technical Implementation

- Webhook-based architecture for real-time updates
- Automatic webhook registration on startup
- User linking via role-based system (Veterinarian = Role 8)
- Markdown formatting for rich messages
- Inline keyboard for interactive menus

---

## ⏰ Automated Scheduler

### Daily Medicine Checks

The system runs automated checks **daily at 9:30 PM Bolivia time (1:30 AM UTC)**:

1. **Stock Monitoring**: Checks all active medications against minimum stock levels
2. **Expiration Tracking**: Calculates days until expiration and sends alerts
3. **Smart Notifications**: Sends aggregated alerts to all registered veterinarians

### Configuration

Located in `app/scheduler.py`:
```python
scheduler.add_job(
    lambda: asyncio.run(verificar_medicamentos()),
    "cron",
    hour=1,   # 01 UTC = 21 Bolivia
    minute=30,
)
```

### Notification Criteria

- **Stock Alert**: `stock <= minStock`
- **Expiration Alert**: Within configured warning period
- **Target Users**: All veterinarians (role 8) with registered Telegram chat_id

---

## 📊 Dashboard & Analytics

### Endpoint: `GET /dashboard`

Returns comprehensive statistics with **30-second cache** for optimal performance.

### Response Structure

```json
{
  "stats": {
    "totalHorses": 50,
    "activeHorses": 45,
    "schoolHorses": 12,
    "totalEmployees": 25,
    "activeEmployees": 23,
    "totalOwners": 35,
    "pendingTasks": 8,
    "completedTasks": 42,
    "monthlyIncome": 125000.50,
    "monthlyExpenses": 87500.25,
    "netBalance": 37500.25
  },
  "tasksSummary": [
    {"status": "Pendiente", "count": 8},
    {"status": "En progreso", "count": 3},
    {"status": "Completada", "count": 42}
  ],
  "recentAttentions": [
    {
      "idAttentionHorse": 123,
      "date": "2026-01-25",
      "description": "Vaccination",
      "cost": 150.00,
      "horseName": "Thunder",
      "employeeName": "Dr. Smith"
    }
  ],
  "monthlyFinancials": [
    {
      "month": "2025-02",
      "income": 120000.00,
      "expenses": 85000.00
    }
  ],
  "dailyFinancials": [
    {
      "date": "2026-01-25",
      "income": 4500.00,
      "expenses": 3200.00
    }
  ]
}
```

### Features

- **Real-time Statistics**: Current counts for all major entities
- **Financial Overview**: 12-month financial history
- **Task Analytics**: Status breakdown of all tasks
- **Recent Activity**: Last 8 horse attentions with joins
- **Daily Trends**: Day-by-day income/expense tracking
- **Performance Optimization**: Smart caching with TTL
- **Concurrent Queries**: Async/await for parallel data fetching

---

## 💡 API Usage Examples

### 1. Register a New Horse

```bash
curl -X POST http://127.0.0.1:8000/horses \
  -H "Content-Type: application/json" \
  -d '{
    "horseName": "Thunder",
    "birthdate": "2020-03-15",
    "sex": "Male",
    "color": "Brown",
    "generalDescription": "Strong racing horse",
    "passportNumber": 123456,
    "box": true,
    "section": false,
    "basket": false,
    "fk_idRace": 1,
    "fk_idOwner": 5,
    "state": "ACTIVO",
    "stateSchool": false
  }'
```

### 2. Create Vaccination Plan

```bash
curl -X POST http://127.0.0.1:8000/vaccination_plan \
  -H "Content-Type: application/json" \
  -d '{
    "planName": "Annual Equine Vaccination",
    "scheduledMonths": [1, 6, 12],
    "dosesByMonth": {"1": 1, "6": 1, "12": 1},
    "alertStatus": "ACTIVE",
    "fk_idMedicine": 3
  }'
```

### 3. Record Horse Attention

```bash
curl -X POST http://127.0.0.1:8000/attention_horse \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-01-27",
    "dose": "10ml",
    "cost": 250.00,
    "description": "Routine vaccination and health check",
    "fk_idHorse": 12,
    "fk_idMedicine": 5,
    "fk_idEmployee": 8
  }'
```

### 4. Add Medicine with Expiration Tracking

```bash
curl -X POST http://127.0.0.1:8000/medicines \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ivermectin",
    "description": "Antiparasitic medication",
    "medicationType": "Injectable",
    "stock": 50,
    "minStock": 10,
    "boxExpirationDate": "2026-12-31",
    "openedOn": "2026-01-15",
    "daysAfterOpening": 90,
    "openedExpirationDate": "2026-04-15",
    "expiryStatus": "ACTIVE",
    "stockStatus": "ADEQUATE",
    "notifyDaysBefore": "2026-04-08",
    "isActive": true,
    "source": "GENERAL"
  }'
```

### 5. Create Employee with Shift

```bash
curl -X POST http://127.0.0.1:8000/employees \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "John Doe",
    "ci": 1234567,
    "phoneNumber": 77123456,
    "startContractDate": "2026-01-01",
    "endContractDate": "2026-12-31",
    "startTime": "2026-01-01T08:00:00",
    "exitTime": "2026-01-01T17:00:00",
    "salary": 3500.00,
    "status": true,
    "fk_idPositionEmployee": 2
  }'
```

### 6. Generate Owner Monthly Report

```bash
curl -X POST http://127.0.0.1:8000/owner_report_month \
  -H "Content-Type: application/json" \
  -d '{
    "period": 202601,
    "priceAlpha": 850.00,
    "box": 500.00,
    "section": 0.00,
    "aBasket": 300.00,
    "contributionCabFlyer": 150.00,
    "VaccineApplication": 200.00,
    "deworming": 100.00,
    "AmeniaExam": 80.00,
    "externalTeacher": 0.00,
    "fine": 0.00,
    "saleChala": 0.00,
    "costPerBucket": 0.00,
    "healthCardPayment": 50.00,
    "other": 0.00,
    "fk_idOwner": 5,
    "state": "PENDING"
  }'
```

### 7. Get Dashboard Analytics

```bash
curl -X GET http://127.0.0.1:8000/dashboard
```

### 8. List Medicines with Pagination

```bash
curl -X GET "http://127.0.0.1:8000/medicines?skip=0&limit=20"
```

---

## 🛠 Development Guidelines

### Code Style

- Follow **PEP 8** guidelines for Python code
- Use **type hints** for all function parameters and returns
- Write **descriptive variable names** and comments where necessary
- Keep functions **small and focused** (single responsibility)

### Environment Management

- **Never commit** `.env` files or secrets to version control
- Use `.env.example` for documenting required environment variables
- Store all secrets in environment variables or secure vaults

### Adding New Features

1. **Schema First**: Define Pydantic models in `schemas/`
2. **CRUD Operations**: Implement database operations in `crud/`
3. **Router Endpoints**: Create API endpoints in `routers/`
4. **Register Router**: Import and register in `main.py`
5. **Test Thoroughly**: Use `/docs` for interactive testing

### Database Changes

1. Modify tables in Supabase dashboard
2. Update `dataSchema.sql` for reference
3. Update corresponding Pydantic schemas
4. Update CRUD operations if needed

### Best Practices

- **Async/Await**: Use async operations for all I/O
- **Error Handling**: Always handle exceptions with proper HTTP status codes
- **Validation**: Let Pydantic handle input validation
- **Pagination**: Use pagination utilities for list endpoints
- **Caching**: Implement caching for expensive operations (like dashboard)
- **Security**: Never expose internal errors to clients in production

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is proprietary software for Country Club ERP management.

---

## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Supabase Documentation](https://supabase.com/docs)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 📧 Support

For questions or issues, please contact the development team or open an issue in the repository.

---

**Built with ❤️ for equestrian facility management**
