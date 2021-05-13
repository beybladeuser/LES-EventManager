@echo off 

FOR /F "tokens=* USEBACKQ" %%F IN (`cd`) DO (
SET folder=%%F
)

FOR /d %%i in ("%folder%\*") do (
	cd %%i
	if exist .\__pycache__ (
		echo Deleting --- %%i\__pycache__
		cd %%i\__pycache__
		del /f /q /s *.* >NUL
		cd ..
		rmdir /q /s .\__pycache__
	) else (
		echo No __pycache__ in %%i
	)

	if exist .\migrations (
		if exist .\migrations\__pycache__ (
			echo Deleting --- %%i\migrations\__pycache__
			cd %%i\migrations\__pycache__
			del /f /q /s *.* >NUL
			cd ..
			rmdir /q /s .\__pycache__
			cd ..
		) else (
			echo No __pycache__ in %%i
		)
		FOR  %%f in ("%%i\migrations\*") do (
			if "%%f" NEQ "%%i\migrations\__init__.py" (
				del /f /q /s "%%f">NUL
			)
		)
	) else (
		echo No migrations in %%i
	)

)

cd %folder%