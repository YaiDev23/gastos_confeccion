class OperatorSchema:
    operaria = {
        'salario': 56000,
    }
    operaria_prestaciones = {
        'salario': 50300,
    }
    aprendiz = {
        'salario': 30000,
    }
        
    operaria: int
    aprendiz: int
    operaria_prestaciones: int  # Nuevo campo para salario con prestaciones