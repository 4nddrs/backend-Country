-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.alpha_control (
  idAlphaControl bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  date date NOT NULL,
  alphaIncome numeric NOT NULL,
  unitPrice numeric NOT NULL,
  totalPurchasePrice numeric NOT NULL,
  outcome numeric NOT NULL,
  balance numeric NOT NULL,
  salePrice numeric NOT NULL,
  income numeric NOT NULL,
  closingAmount text NOT NULL,
  fk_idFoodProvider bigint NOT NULL,
  CONSTRAINT alpha_control_pkey PRIMARY KEY (idAlphaControl),
  CONSTRAINT alpha_control_fk_idFoodProvider_fkey FOREIGN KEY (fk_idFoodProvider) REFERENCES public.food_provider(idFoodProvider)
);
CREATE TABLE public.application_procedure (
  idApplicationProcedure bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  executionDate date NOT NULL,
  observations character varying,
  fk_idScheduledProcedure bigint NOT NULL,
  fk_idHorse bigint NOT NULL,
  CONSTRAINT application_procedure_pkey PRIMARY KEY (idApplicationProcedure),
  CONSTRAINT application_procedure_fk_idHorse_fkey FOREIGN KEY (fk_idHorse) REFERENCES public.horse(idHorse),
  CONSTRAINT application_procedure_fk_idScheduledProcedure_fkey FOREIGN KEY (fk_idScheduledProcedure) REFERENCES public.scheduled_procedure(idScheduledProcedure)
);
CREATE TABLE public.attention_horse (
  idAttentionHorse bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  date date NOT NULL,
  dose character varying NOT NULL,
  cost numeric NOT NULL,
  description character varying NOT NULL,
  fk_idHorse bigint NOT NULL,
  fk_idMedicine bigint,
  fk_idEmployee bigint NOT NULL,
  CONSTRAINT attention_horse_pkey PRIMARY KEY (idAttentionHorse),
  CONSTRAINT attention_horse_fk_idHorse_fkey FOREIGN KEY (fk_idHorse) REFERENCES public.horse(idHorse),
  CONSTRAINT attention_horse_fk_idEmployee_fkey FOREIGN KEY (fk_idEmployee) REFERENCES public.employee(idEmployee),
  CONSTRAINT attention_horse_fk_idMedicine_fkey FOREIGN KEY (fk_idMedicine) REFERENCES public.medicine(idMedicine)
);
CREATE TABLE public.employee (
  idEmployee bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  fullName character varying NOT NULL,
  ci character varying NOT NULL,
  phoneNumber smallint NOT NULL,
  employeePhoto bytea,
  startContractDate date NOT NULL,
  endContractDate date NOT NULL,
  startTime timestamp without time zone NOT NULL,
  exitTime timestamp without time zone NOT NULL,
  salary smallint NOT NULL,
  status boolean DEFAULT false,
  fk_idPositionEmployee bigint NOT NULL,
  CONSTRAINT employee_pkey PRIMARY KEY (idEmployee),
  CONSTRAINT employee_fk_idPositionEmployee_fkey FOREIGN KEY (fk_idPositionEmployee) REFERENCES public.employee_position(idPositionEmployee)
);
CREATE TABLE public.employee_absence (
  idEmployeeAbsence bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  startDate date NOT NULL,
  endDate date NOT NULL,
  isVacation boolean NOT NULL,
  absent boolean NOT NULL,
  observation character varying NOT NULL,
  fk_idEmployee bigint NOT NULL,
  CONSTRAINT employee_absence_pkey PRIMARY KEY (idEmployeeAbsence),
  CONSTRAINT employee_absence_fk_idEmployee_fkey FOREIGN KEY (fk_idEmployee) REFERENCES public.employee(idEmployee)
);
CREATE TABLE public.employee_position (
  idPositionEmployee bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  namePosition character varying NOT NULL,
  CONSTRAINT employee_position_pkey PRIMARY KEY (idPositionEmployee)
);
CREATE TABLE public.employees_shiftem (
  idEmployeesShiftem bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  fk_idEmployee bigint,
  fk_idShiftEmployees bigint,
  CONSTRAINT employees_shiftem_pkey PRIMARY KEY (idEmployeesShiftem),
  CONSTRAINT employees_shiftem_fk_idEmployee_fkey FOREIGN KEY (fk_idEmployee) REFERENCES public.employee(idEmployee),
  CONSTRAINT employees_shiftem_fk_idShiftEmployees_fkey FOREIGN KEY (fk_idShiftEmployees) REFERENCES public.shift_employed(idShiftEmployed)
);
CREATE TABLE public.erp_user (
  idErpUser bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  username character varying NOT NULL,
  email character varying NOT NULL,
  fk_idOwner bigint,
  fk_idEmployee bigint,
  fk_idAuthUser uuid,
  fk_idUserRole bigint NOT NULL,
  CONSTRAINT erp_user_pkey PRIMARY KEY (idErpUser),
  CONSTRAINT erp_user_fk_idUserRole_fkey FOREIGN KEY (fk_idUserRole) REFERENCES public.user_role(idUserRole),
  CONSTRAINT erp_user_fk_idAuthUser_fkey FOREIGN KEY (fk_idAuthUser) REFERENCES auth.users(id),
  CONSTRAINT erp_user_fk_idEmployee_fkey FOREIGN KEY (fk_idEmployee) REFERENCES public.employee(idEmployee),
  CONSTRAINT erp_user_fk_idOwner_fkey FOREIGN KEY (fk_idOwner) REFERENCES public.owner(idOwner)
);
CREATE TABLE public.expenses (
  idExpenses bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  date date NOT NULL,
  description character varying NOT NULL,
  AmountBsCaptureType numeric NOT NULL,
  period date NOT NULL,
  CONSTRAINT expenses_pkey PRIMARY KEY (idExpenses)
);
CREATE TABLE public.food_provider (
  idFoodProvider bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  supplierName character varying NOT NULL,
  cellphoneNumber integer NOT NULL,
  generalDescription character varying,
  CONSTRAINT food_provider_pkey PRIMARY KEY (idFoodProvider)
);
CREATE TABLE public.food_stock (
  idFood bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  foodName character varying NOT NULL,
  stock bigint NOT NULL,
  unitMeasurement numeric NOT NULL,
  minStock bigint NOT NULL,
  maxStock bigint NOT NULL,
  fk_idFoodProvider bigint NOT NULL,
  CONSTRAINT food_stock_pkey PRIMARY KEY (idFood),
  CONSTRAINT food_stock_fk_idFoodProvider_fkey FOREIGN KEY (fk_idFoodProvider) REFERENCES public.food_provider(idFoodProvider)
);
CREATE TABLE public.horse (
  idHorse bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  horseName character varying NOT NULL,
  horsePhoto bytea,
  birthdate date NOT NULL,
  sex character varying NOT NULL,
  color character varying NOT NULL,
  generalDescription character varying NOT NULL,
  passportNumber bigint,
  box boolean,
  section boolean,
  basket boolean,
  fk_idRace bigint NOT NULL,
  fk_idOwner bigint NOT NULL,
  fl_idNutritionalPlan bigint,
  CONSTRAINT horse_pkey PRIMARY KEY (idHorse),
  CONSTRAINT horse_fl_idNutritionalPlan_fkey FOREIGN KEY (fl_idNutritionalPlan) REFERENCES public.nutritional_plan(idNutritionalPlan),
  CONSTRAINT horse_fk_idRace_fkey FOREIGN KEY (fk_idRace) REFERENCES public.race(idRace),
  CONSTRAINT horse_fk_idOwner_fkey FOREIGN KEY (fk_idOwner) REFERENCES public.owner(idOwner)
);
CREATE TABLE public.income (
  idIncome bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  date date NOT NULL,
  description character varying NOT NULL,
  amountBsCaptureType numeric NOT NULL,
  period date NOT NULL,
  CONSTRAINT income_pkey PRIMARY KEY (idIncome)
);
CREATE TABLE public.medicine (
  idMedicine bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name character varying NOT NULL,
  description character varying,
  medicationType character varying,
  stock bigint NOT NULL,
  minStock bigint NOT NULL,
  boxExpirationDate date NOT NULL,
  openedOn date NOT NULL,
  daysAfterOpening bigint NOT NULL,
  openedExpirationDate date NOT NULL,
  expiryStatus character varying NOT NULL,
  stockStatus character varying NOT NULL,
  notifyDaysBefore date NOT NULL,
  isActive boolean,
  source character varying,
  fk_idHorse bigint,
  CONSTRAINT medicine_pkey PRIMARY KEY (idMedicine),
  CONSTRAINT medicine_fk_idHorse_fkey FOREIGN KEY (fk_idHorse) REFERENCES public.horse(idHorse)
);
CREATE TABLE public.nutritional_plan (
  idNutritionalPlan bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name character varying NOT NULL,
  description character varying,
  assignmentDate date NOT NULL,
  endDate date NOT NULL,
  state character varying NOT NULL,
  CONSTRAINT nutritional_plan_pkey PRIMARY KEY (idNutritionalPlan)
);
CREATE TABLE public.nutritional_plan_details (
  idDetail bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  consumptionKlg numeric NOT NULL,
  daysConsumptionMonth bigint NOT NULL,
  totalConsumption numeric NOT NULL,
  period date NOT NULL,
  fk_idFood bigint NOT NULL,
  fk_idNutritionalPlan bigint NOT NULL,
  CONSTRAINT nutritional_plan_details_pkey PRIMARY KEY (idDetail),
  CONSTRAINT nutritional_plan_details_fk_idNutritionalPlan_fkey FOREIGN KEY (fk_idNutritionalPlan) REFERENCES public.nutritional_plan(idNutritionalPlan),
  CONSTRAINT nutritional_plan_details_fk_idFood_fkey FOREIGN KEY (fk_idFood) REFERENCES public.food_stock(idFood)
);
CREATE TABLE public.owner (
  idOwner bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name character varying NOT NULL,
  FirstName character varying NOT NULL,
  SecondName character varying,
  ci bigint NOT NULL,
  phoneNumber bigint NOT NULL,
  ownerPhoto bytea,
  CONSTRAINT owner_pkey PRIMARY KEY (idOwner)
);
CREATE TABLE public.owner_report_month (
  idOwnerReportMonth bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  period numeric NOT NULL,
  daysAlphaConsumption numeric NOT NULL,
  quantityAlphaKg numeric NOT NULL,
  priceAlpha numeric NOT NULL,
  box numeric NOT NULL,
  section numeric NOT NULL,
  aBasket numeric NOT NULL,
  contributionCabFlyer numeric NOT NULL,
  VaccineApplication numeric NOT NULL,
  deworming numeric NOT NULL,
  AmeniaExam numeric NOT NULL,
  externalTeacher numeric NOT NULL,
  fine numeric NOT NULL,
  saleChala numeric NOT NULL,
  costPerBucket numeric NOT NULL,
  healthCardPayment numeric NOT NULL,
  other numeric NOT NULL,
  fk_idOwner bigint NOT NULL,
  CONSTRAINT owner_report_month_pkey PRIMARY KEY (idOwnerReportMonth),
  CONSTRAINT owner_report_month_fk_idOwner_fkey FOREIGN KEY (fk_idOwner) REFERENCES public.owner(idOwner)
);
CREATE TABLE public.race (
  idRace bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  nameRace character varying NOT NULL,
  CONSTRAINT race_pkey PRIMARY KEY (idRace)
);
CREATE TABLE public.scheduled_procedure (
  idScheduledProcedure bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  year date NOT NULL,
  name character varying NOT NULL,
  description character varying,
  scheduledMonths jsonb NOT NULL,
  alertLabel character varying NOT NULL,
  CONSTRAINT scheduled_procedure_pkey PRIMARY KEY (idScheduledProcedure)
);
CREATE TABLE public.shift_employed (
  idShiftEmployed bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  startDateTime timestamp without time zone NOT NULL,
  endDateTime timestamp without time zone NOT NULL,
  fk_idShiftType bigint NOT NULL,
  CONSTRAINT shift_employed_pkey PRIMARY KEY (idShiftEmployed),
  CONSTRAINT shift_employed_fk_idShiftType_fkey FOREIGN KEY (fk_idShiftType) REFERENCES public.shift_type(idShiftType)
);
CREATE TABLE public.shift_type (
  idShiftType bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  shiftName character varying NOT NULL,
  description character varying,
  CONSTRAINT shift_type_pkey PRIMARY KEY (idShiftType)
);
CREATE TABLE public.task (
  idTask bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  taskName character varying NOT NULL,
  description character varying,
  assignmentDate date NOT NULL,
  completionDate date NOT NULL,
  taskStatus character varying NOT NULL,
  fk_idTaskCategory bigint NOT NULL,
  fk_idEmployee bigint,
  CONSTRAINT task_pkey PRIMARY KEY (idTask),
  CONSTRAINT task_fk_idEmployee_fkey FOREIGN KEY (fk_idEmployee) REFERENCES public.employee(idEmployee),
  CONSTRAINT task_fk_idTaskCategory_fkey FOREIGN KEY (fk_idTaskCategory) REFERENCES public.task_category(idTaskCategory)
);
CREATE TABLE public.task_category (
  idTaskCategory bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  categoryName character varying NOT NULL,
  description character varying,
  CONSTRAINT task_category_pkey PRIMARY KEY (idTaskCategory)
);
CREATE TABLE public.total_control (
  idTotalControl bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  toCaballerizo numeric NOT NULL,
  vaccines numeric NOT NULL,
  anemia numeric NOT NULL,
  deworming numeric NOT NULL,
  consumptionAlfaDiaKlg numeric NOT NULL,
  costAlfaBs numeric NOT NULL,
  daysConsumptionMonth numeric NOT NULL,
  consumptionAlphaMonthKlg numeric NOT NULL,
  costTotalAlphaBs numeric NOT NULL,
  cubeChala numeric NOT NULL,
  UnitCostChalaBs numeric NOT NULL,
  costTotalChalaBs numeric NOT NULL,
  totalCharge numeric NOT NULL,
  fk_idOwner bigint NOT NULL,
  fk_idHorse bigint NOT NULL,
  CONSTRAINT total_control_pkey PRIMARY KEY (idTotalControl),
  CONSTRAINT total_control_fk_idOwner_fkey FOREIGN KEY (fk_idOwner) REFERENCES public.owner(idOwner),
  CONSTRAINT total_control_fk_idHorse_fkey FOREIGN KEY (fk_idHorse) REFERENCES public.horse(idHorse)
);
CREATE TABLE public.user_role (
  idUserRole bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  roleName character varying NOT NULL,
  CONSTRAINT user_role_pkey PRIMARY KEY (idUserRole)
);
CREATE TABLE public.vaccination_plan (
  idVaccinationPlan bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  planName character varying NOT NULL,
  scheduledMonths jsonb NOT NULL,
  dosesByMonth json NOT NULL,
  alertStatus character varying NOT NULL,
  fk_idMedicine bigint NOT NULL,
  CONSTRAINT vaccination_plan_pkey PRIMARY KEY (idVaccinationPlan),
  CONSTRAINT vaccination_plan_fk_idMedicine_fkey FOREIGN KEY (fk_idMedicine) REFERENCES public.medicine(idMedicine)
);
CREATE TABLE public.vaccination_plan_application (
  idVaccinationPlanApplication bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  applicationDate date NOT NULL,
  observation character varying,
  fk_idVaccinationPlan bigint NOT NULL,
  fk_idHorse bigint NOT NULL,
  fk_idEmployee bigint NOT NULL,
  CONSTRAINT vaccination_plan_application_pkey PRIMARY KEY (idVaccinationPlanApplication),
  CONSTRAINT vaccination plan application_fk_idHorse_fkey FOREIGN KEY (fk_idHorse) REFERENCES public.horse(idHorse),
  CONSTRAINT vaccination plan application_fk_idEmployee_fkey FOREIGN KEY (fk_idEmployee) REFERENCES public.employee(idEmployee),
  CONSTRAINT vaccination plan application_fk_idVaccinationPlan_fkey FOREIGN KEY (fk_idVaccinationPlan) REFERENCES public.vaccination_plan(idVaccinationPlan)
);