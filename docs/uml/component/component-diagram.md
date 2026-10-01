# Component Diagram

## CCMS Architecture

```mermaid
flowchart TD
    %% Client Layer
    subgraph Client [Client Layer (Browser)]
        React[React Frontend App]
        subgraph Modules [UI Modules]
            AuthM(Auth Module)
            CompM(Complaint Module)
            DashM(Dashboard Module)
            MaintM(Maintenance Module)
        end
        React --- Modules
    end

    %% API Layer
    subgraph API [API Gateway]
        Express[Express REST API]
        Multer[Multer (File Uploads)]
    end

    %% Business Layer
    subgraph Business [Business Layer]
        Controllers[Route Controllers]
        Services[Business Services]
        Validators[Data Validators]
    end

    %% Data Layer
    subgraph Data [Data Layer]
        ORM[Sequelize/TypeORM]
        MySQL[(MySQL Database)]
    end

    %% Dependencies
    AuthM & CompM & DashM & MaintM -->|HTTP/REST| Express
    Express --> Multer
    Express --> Controllers
    Controllers --> Validators
    Controllers --> Services
    Services --> ORM
    ORM --> MySQL
```
