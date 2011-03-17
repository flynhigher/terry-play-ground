if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[usp_insert_property]') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
drop procedure [dbo].[usp_insert_property]
GO

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
GRANT EXECUTE ON usp_insert_property TO urole_execute