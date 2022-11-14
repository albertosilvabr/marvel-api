CREATE TABLE comics (
        id                 bigint(20)   NULL,
        digitalid          bigint(20)   NULL,
        title              varchar(999) NULL,
        issuenumber        int          NULL,
        variantgescription varchar(999) NULL,
        description        MEDIUMTEXT   NULL,
        modified           varchar(50)  NULL,
        diamondcode        varchar(100) NULL,        
        isbn               varchar(100) NULL,
        upc                varchar(100) NULL,
        ean                varchar(100) NULL,
        issn               varchar(100) NULL,        
        formatt            varchar(50)  NULL,
        pagecount          INT          NULL,
        resourceuri        varchar(100) NULL,
        characterId        bigint(20)   NULL,
        charactername      varchar(100) NULL

); 