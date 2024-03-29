use [REMap]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[FK_Property_Revision_REProperty]') and OBJECTPROPERTY(id, N'IsForeignKey') = 1)
ALTER TABLE [dbo].[Property_Revision] DROP CONSTRAINT FK_Property_Revision_REProperty
GO

/****** Object:  Stored Procedure dbo.usp_insert_property    Script Date: 2/9/2007 12:24:58 AM ******/
if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[usp_insert_property]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[usp_insert_property]
GO

/****** Object:  Table [dbo].[Property_Revision]    Script Date: 2/9/2007 12:24:58 AM ******/
if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[Property_Revision]') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
drop table [dbo].[Property_Revision]
GO

/****** Object:  Table [dbo].[REProperty]    Script Date: 2/9/2007 12:24:58 AM ******/
if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[REProperty]') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
drop table [dbo].[REProperty]
GO

/****** Object:  Login REMap_User    Script Date: 2/9/2007 12:24:53 AM ******/
if not exists (select * from master.dbo.syslogins where loginname = N'REMap_User')
BEGIN
	declare @logindb nvarchar(132), @loginlang nvarchar(132) select @logindb = N'REMap', @loginlang = N'us_english'
	if @logindb is null or not exists (select * from master.dbo.sysdatabases where name = @logindb)
		select @logindb = N'master'
	if @loginlang is null or (not exists (select * from master.dbo.syslanguages where name = @loginlang) and @loginlang <> N'us_english')
		select @loginlang = @@language
	exec sp_addlogin N'REMap_User', null, @logindb, @loginlang
END
GO

/****** Object:  User dbo    Script Date: 2/9/2007 12:24:53 AM ******/
/****** Object:  User REMap_User    Script Date: 2/9/2007 12:24:53 AM ******/
if not exists (select * from dbo.sysusers where name = N'REMap_User' and uid < 16382)
	EXEC sp_grantdbaccess N'REMap_User', N'REMap_User'
GO

/****** Object:  DatabaseRole urole_execute    Script Date: 2/9/2007 12:24:53 AM ******/
if not exists (select * from dbo.sysusers where name = N'urole_execute' and uid > 16399)
	EXEC sp_addrole N'urole_execute'
GO

/****** Object:  User REMap_User    Script Date: 2/9/2007 12:24:53 AM ******/
exec sp_addrolemember N'db_datareader', N'REMap_User'
GO

/****** Object:  User REMap_User    Script Date: 2/9/2007 12:24:53 AM ******/
exec sp_addrolemember N'db_datawriter', N'REMap_User'
GO

/****** Object:  User REMap_User    Script Date: 2/9/2007 12:24:53 AM ******/
exec sp_addrolemember N'urole_execute', N'REMap_User'
GO

/****** Object:  Table [dbo].[REProperty]    Script Date: 2/9/2007 12:24:59 AM ******/
CREATE TABLE [dbo].[REProperty] (
	[Source] [nchar] (10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL ,
	[Id] [nchar] (10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL ,
	[Price] [int] NULL ,
	[Style] [nchar] (20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[Bed] [int] NULL ,
	[Bath] [int] NULL ,
	[StreetAddress] [nvarchar] (200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[Town] [nvarchar] (100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[State] [nvarchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[Zipcode] [nvarchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[Url] [nvarchar] (500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[PhotoUrl] [nvarchar] (500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[Status] [nchar] (10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[Longitude] [nchar] (20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[Latitude] [nchar] (20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[CreatedDate] [datetime] NULL ,
	[Description] [ntext] COLLATE SQL_Latin1_General_CP1_CI_AS NULL 
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

/****** Object:  Table [dbo].[Property_Revision]    Script Date: 2/9/2007 12:25:00 AM ******/
CREATE TABLE [dbo].[Property_Revision] (
	[Id] [int] IDENTITY (1, 1) NOT NULL ,
	[Price] [int] NULL ,
	[Status] [nchar] (10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[RevisedDate] [datetime] NULL ,
	[REProperty_Source] [nchar] (10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[REProperty_Id] [nchar] (10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL 
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[REProperty] WITH NOCHECK ADD 
	CONSTRAINT [PK_REProperty] PRIMARY KEY  CLUSTERED 
	(
		[Source],
		[Id]
	)  ON [PRIMARY] 
GO

ALTER TABLE [dbo].[Property_Revision] WITH NOCHECK ADD 
	CONSTRAINT [PK_REProperty_Revision] PRIMARY KEY  CLUSTERED 
	(
		[Id]
	)  ON [PRIMARY] 
GO

ALTER TABLE [dbo].[Property_Revision] ADD 
	CONSTRAINT [FK_Property_Revision_REProperty] FOREIGN KEY 
	(
		[REProperty_Source],
		[REProperty_Id]
	) REFERENCES [dbo].[REProperty] (
		[Source],
		[Id]
	)
GO

SET QUOTED_IDENTIFIER ON 
GO
SET ANSI_NULLS ON 
GO

/****** Object:  Stored Procedure dbo.usp_insert_property    Script Date: 2/9/2007 12:25:01 AM ******/

CREATE PROCEDURE dbo.usp_insert_property
(
	@Source NCHAR(10),
	@Id NCHAR(10),
	@Price INT,
	@Style NCHAR(20),
	@Bed INT,
	@Bath INT,
	@StreetAddress NVARCHAR(200),
	@Town NVARCHAR(100),
	@State NVARCHAR(50),
	@Zipcode NVARCHAR(50),
	@Url NVARCHAR(500),
	@PhotoUrl NVARCHAR(500),
	@Status NCHAR(10),
	@Longitude NCHAR(20),
	@Latitude NCHAR(20),
	@Description NTEXT
)
AS
	DECLARE @Prev_Price INT
	SET @Prev_Price = 0
	DECLARE @Prev_Status NVARCHAR(10)
	
	SELECT TOP 1 @Prev_Price = Price, @Prev_Status = Status FROM Property_Revision
	WHERE REProperty_Source = @Source AND REProperty_Id = @Id
	ORDER BY RevisedDate DESC
	
	BEGIN TRAN
	IF @Prev_Price > 0
	BEGIN
		IF @Prev_Price <> @Price OR @Prev_Status <> @Status
		BEGIN
			UPDATE REProperty
			SET Price = @Price,
				Status = @Status
			WHERE Source = @Source AND Id = @Id

    IF (@@ERROR <> 0) ROLLBACK TRAN

			INSERT Property_Revision
			(Price, Status, RevisedDate, REProperty_Source, REProperty_Id)
			VALUES
			(@Price, @Status, GETDATE(), @Source, @Id)

    IF (@@ERROR <> 0) ROLLBACK TRAN

		END
	END
	ELSE
	BEGIN
		INSERT REProperty
		(Source, Id, Price, Style, Bed, Bath, StreetAddress, Town, State, Zipcode, Url, PhotoUrl, Status, Longitude, Latitude, CreatedDate, Description)
		VALUES
		(@Source, @Id, @Price, @Style, @Bed, @Bath, @StreetAddress, @Town, @State, @Zipcode, @Url, @PhotoUrl, @Status, @Longitude, @Latitude, GETDATE(), @Description)

    IF (@@ERROR <> 0) ROLLBACK TRAN

		INSERT Property_Revision
		(Price, Status, RevisedDate, REProperty_Source, REProperty_Id)
		VALUES
		(@Price, @Status, GETDATE(), @Source, @Id)

    IF (@@ERROR <> 0) ROLLBACK TRAN

	END
	COMMIT TRAN


GO

SET QUOTED_IDENTIFIER OFF 
GO
SET ANSI_NULLS ON 
GO

GRANT  EXECUTE  ON [dbo].[usp_insert_property]  TO [urole_execute]
GO

