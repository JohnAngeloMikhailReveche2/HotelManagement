CREATE TABLE GUEST (
    GuestID         INTEGER       PRIMARY KEY AUTOINCREMENT
                                  NOT NULL,
    FName           VARCHAR (100) NOT NULL,
    MName           VARCHAR (100) NULL,
    LName           VARCHAR (100) NOT NULL,
    PhoneNumber     VARCHAR (40)  NULL,
    Proof_ID_Type   VARCHAR (60)  NOT NULL,
    Proof_ID_Number VARCHAR (60)  NOT NULL,
    Street          VARCHAR (60)  NOT NULL,
    Barangay        VARCHAR (60)  NULL,
    Zip             VARCHAR (60)  NULL,
    City            VARCHAR (60)  NOT NULL,
    Gender          VARCHAR (30)  NULL,
    IsDeleted       BOOL          NOT NULL
);
