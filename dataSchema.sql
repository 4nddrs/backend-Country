-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

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
  fk_idRoleEmployee bigint NOT NULL,
  fk_idPositionEmployee bigint NOT NULL,
  CONSTRAINT employee_pkey PRIMARY KEY (idEmployee),
  CONSTRAINT employee_fk_idRoleEmployee_fkey FOREIGN KEY (fk_idRoleEmployee) REFERENCES public.employee_role(idRoleEmployee),
  CONSTRAINT employee_fk_idPositionEmployee_fkey FOREIGN KEY (fk_idPositionEmployee) REFERENCES public.employee_position(idPositionEmployee)
);
CREATE TABLE public.employee_position (
  idPositionEmployee bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  namePosition character varying NOT NULL,
  CONSTRAINT employee_position_pkey PRIMARY KEY (idPositionEmployee)
);
CREATE TABLE public.employee_role (
  idRoleEmployee bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  nameRole character varying NOT NULL,
  CONSTRAINT employee_role_pkey PRIMARY KEY (idRoleEmployee)
);
CREATE TABLE public.food_provider (
  idFoodProvider bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  supplierName character varying NOT NULL,
  cellphoneNumber smallint NOT NULL,
  generalDescription character varying,
  CONSTRAINT food_provider_pkey PRIMARY KEY (idFoodProvider)
);
CREATE TABLE public.food_stock (
  idFood bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  foodName character varying NOT NULL,
  stock bigint NOT NULL,
  unitMeasurement numeric NOT NULL,
  unitPrice numeric NOT NULL,
  fk_idFoodProvider bigint NOT NULL,
  CONSTRAINT food_stock_pkey PRIMARY KEY (idFood),
  CONSTRAINT food_stock_fk_idFoodProvider_fkey FOREIGN KEY (fk_idFoodProvider) REFERENCES public.food_provider(idFoodProvider)
);
CREATE TABLE public.horse (
  idHorse bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  horseName character varying NOT NULL,
  horsePhoto bytea,
  dirthDate date NOT NULL,
  sex character varying NOT NULL,
  color character varying NOT NULL,
  generalDescription character varying NOT NULL,
  fk_idOwner bigint NOT NULL,
  fk_idRace bigint NOT NULL,
  fk_idVaccine bigint,
  fk_idEmployee bigint NOT NULL,
  CONSTRAINT horse_pkey PRIMARY KEY (idHorse),
  CONSTRAINT horse_fk_idEmployee_fkey FOREIGN KEY (fk_idEmployee) REFERENCES public.employee(idEmployee),
  CONSTRAINT horse_fk_idOwner_fkey FOREIGN KEY (fk_idOwner) REFERENCES public.owner(idOwner),
  CONSTRAINT horse_fk_idVaccine_fkey FOREIGN KEY (fk_idVaccine) REFERENCES public.vaccine(idVaccine),
  CONSTRAINT horse_fk_idRace_fkey FOREIGN KEY (fk_idRace) REFERENCES public.race(idRace)
);
CREATE TABLE public.nutritionalPlan_horse (
  idNutritionalPlan_horse bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  assignmentDate date NOT NULL,
  fk_idNutritionalPlan bigint NOT NULL,
  fk_idHorse bigint NOT NULL,
  CONSTRAINT nutritionalPlan_horse_pkey PRIMARY KEY (idNutritionalPlan_horse),
  CONSTRAINT nutritionalPlan_horse_fk_idHorse_fkey FOREIGN KEY (fk_idHorse) REFERENCES public.horse(idHorse),
  CONSTRAINT nutritionalPlan_horse_fk_idNutritionalPlan_fkey FOREIGN KEY (fk_idNutritionalPlan) REFERENCES public.nutritional_plan(idNutritionalPlan)
);
CREATE TABLE public.nutritional_plan (
  idNutritionalPlan bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name character varying NOT NULL,
  startDate date NOT NULL,
  endDate date NOT NULL,
  description character varying,
  CONSTRAINT nutritional_plan_pkey PRIMARY KEY (idNutritionalPlan)
);
CREATE TABLE public.nutritional_plan_details (
  idDetail bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  amount numeric NOT NULL,
  frequency character varying NOT NULL,
  schedule timestamp without time zone NOT NULL,
  fk_idFood bigint NOT NULL,
  fk_idNutritionalPlan bigint,
  CONSTRAINT nutritional_plan_details_pkey PRIMARY KEY (idDetail),
  CONSTRAINT nutritional_plan_details_fk_idFood_fkey FOREIGN KEY (fk_idFood) REFERENCES public.food_stock(idFood),
  CONSTRAINT nutritional_plan_details_fk_idNutritionalPlan_fkey FOREIGN KEY (fk_idNutritionalPlan) REFERENCES public.nutritional_plan(idNutritionalPlan)
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
CREATE TABLE public.product (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  name character varying NOT NULL,
  CONSTRAINT product_pkey PRIMARY KEY (id)
);
CREATE TABLE public.race (
  idRace bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  nameRace character varying NOT NULL,
  CONSTRAINT race_pkey PRIMARY KEY (idRace)
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
  CONSTRAINT task_fk_idTaskCategory_fkey FOREIGN KEY (fk_idTaskCategory) REFERENCES public.task_category(idTaskCategory),
  CONSTRAINT task_fk_idEmployee_fkey FOREIGN KEY (fk_idEmployee) REFERENCES public.employee(idEmployee)
);
CREATE TABLE public.task_category (
  idTaskCategory bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  categoryName character varying NOT NULL,
  description character varying,
  CONSTRAINT task_category_pkey PRIMARY KEY (idTaskCategory)
);
CREATE TABLE public.vaccine (
  idVaccine bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  vaccineName character varying NOT NULL,
  vaccineType character varying NOT NULL,
  CONSTRAINT vaccine_pkey PRIMARY KEY (idVaccine)
);