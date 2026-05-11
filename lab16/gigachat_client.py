"""
Клиент для работы с GigaChat API
Поддерживает генерацию кода, рефакторинг, создание тестов и документации
"""
from token_dla_gigachat import token
import os
import json
from dotenv import load_dotenv
from gigachat import GigaChat
from typing import List, Dict, Optional

# Загрузка переменных окружения
load_dotenv(encoding='utf-8')


class GigaChatAssistant:
    """Ассистент на основе GigaChat для задач разработки"""
    
    def __init__(self):
        self.credentials = os.getenv("GIGACHAT_CREDENTIALS")
        self.scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
        self.model = os.getenv("GIGACHAT_MODEL", "GigaChat-2")
        self.verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "False").lower() == "true"
        
        # TODO: Инициализация клиента GigaChat
        # Ваш код:
        self.client = GigaChat(
            credentials=token,#self.credentials,
            scope=self.scope,
            model=self.model,
            verify_ssl_certs=self.verify_ssl
        )
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """
        Генерация кода по текстовому описанию
        
        Args:
            description: Описание требуемой функции/класса
            language: Язык программирования
            
        Returns:
            Сгенерированный код
        """
        # TODO: Сформировать промпт и отправить запрос к GigaChat
        # Ваш код:
        prompt = f"""
        Ты — эксперт по разработке на {language}. Напиши код на {language} для следующей задачи:
        
        {description}
        
        Требования к коду:
        - Добавь аннотации типов (для Python)
        - Добавь docstring с описанием функции, параметров и возвращаемого значения
        - Используй понятные имена переменных
        - Добавь обработку ошибок
        
        Верни только код, без пояснений.
        """
        
        response = self.client.chat(prompt)
        code = response.choices[0].message.content
        
        # Очистка от markdown-разметки, если есть
        if code.startswith("```"):
            code = code.split("```")[1]
            if code.startswith(language):
                code = code[len(language):]
            code = code.strip()
        
        return code
    
    def refactor_code(self, code: str, requirements: str) -> str:
        """
        Рефакторинг существующего кода
        
        Args:
            code: Исходный код для рефакторинга
            requirements: Требования к рефакторингу
            
        Returns:
            Отрефакторенный код
        """
        # TODO: Сформировать промпт для рефакторинга
        # Ваш код:
        prompt = f"""
        Проведи рефакторинг следующего кода согласно требованиям.
        
        Исходный код:
        ```python
        {code}
        ```
        
        Требования к рефакторингу:
        {requirements}
        
        Дополнительные требования:
        - Сохрани исходную функциональность
        - Улучши читаемость кода
        - Добавь аннотации типов (если их нет)
        - Разбей на более мелкие функции (если необходимо)
        - Добавь обработку ошибок
        
        Верни только отрефакторенный код, без пояснений.
        """
        
        response = self.client.chat(prompt)
        refactored = response.choices[0].message.content
        
        # Очистка от markdown-разметки
        if refactored.startswith("```"):
            refactored = refactored.split("```")[1]
            if refactored.startswith("python"):
                refactored = refactored[6:]
            refactored = refactored.strip()
        
        return refactored
    
    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        """
        Генерация тестов для кода
        
        Args:
            code: Исходный код
            framework: Тестовый фреймворк (pytest, unittest)
            
        Returns:
            Код с тестами
        """
        # TODO: Сформировать промпт для генерации тестов
        # Ваш код:
        prompt = f"""
        Напиши тесты для следующего кода, используя {framework}.
        
        Код для тестирования:
        ```python
        {code}
        ```
        
        Требования к тестам:
        - Протестируй все публичные функции
        - Включи позитивные и негативные сценарии
        - Проверь граничные случаи
        - Добавь понятные названия тестов
        
        Верни только код с тестами, без пояснений.
        и не дописывай новых функций
        """
        
        response = self.client.chat(prompt)
        tests = response.choices[0].message.content
        
        if tests.startswith("```"):
            tests = tests.split("```")[1]
            if tests.startswith(framework) or tests.startswith("python"):
                tests = tests.split("\n", 1)[1] if "\n" in tests else tests
            tests = tests.strip()
        
        return tests
    
    def generate_documentation(self, code: str, doc_type: str = "docstring") -> str:
        """
        Генерация документации для кода
        
        Args:
            code: Исходный код
            doc_type: Тип документации (docstring, readme, api)
            
        Returns:
            Сгенерированная документация
        """
        # TODO: Сформировать промпт для генерации документации
        # Ваш код:
        if doc_type == "docstring":
            prompt = f"""
            Добавь docstring для каждой функции в следующем коде.
            
            Код:
            ```python
            {code}
            ```
            
            Формат docstring (Google Style):
            def function(param1: type, param2: type) -> return_type:
                \"\"\"Краткое описание.
                
                Args:
                    param1: Описание параметра 1
                    param2: Описание параметра 2
                
                Returns:
                    Описание возвращаемого значения
                
                Raises:
                    ExceptionType: Когда возникает исключение
                \"\"\"
            
            Верни полный код с добавленными docstring.
            """
        else:
            prompt = f"""
            Создай README документацию для следующего кода.
            
            Код:
            ```python
            {code}
            ```
            
            Включи в документацию:
            - Описание назначения кода
            - Инструкцию по установке зависимостей
            - Примеры использования
            - Описание основных функций
            - Информацию об авторах (если есть)
            """
        
        response = self.client.chat(prompt)
        documentation = response.choices[0].message.content
        
        if doc_type == "docstring" and documentation.startswith("```"):
            documentation = documentation.split("```")[1]
            if documentation.startswith("python"):
                documentation = documentation[6:]
            documentation = documentation.strip()
        
        return documentation
    
    def analyze_code(self, code: str) -> Dict[str, List[str]]:
        """
        Анализ качества, читаемости и потенциальных уязвимостей
        
        Args:
            code: Исходный код для анализа
            
        Returns:
            Словарь с результатами анализа
        """
        # TODO: Сформировать промпт для анализа кода
        # Ваш код:
        prompt = f"""
        Проанализируй следующий код и верни результат в формате JSON.
        
        Код:
        ```python
        {code}
        ```
        
        Оцени следующие аспекты:
        1. quality_issues: проблемы качества кода (нарушения PEP8, длинные функции и т.д.)
        2. readability_issues: проблемы читаемости (плохие имена переменных, отсутствие комментариев)
        3. security_issues: потенциальные уязвимости (инъекции, небезопасные функции)
        4. performance_issues: проблемы производительности (неэффективные алгоритмы)
        5. suggestions: конкретные предложения по улучшению
        
        Формат ответа (JSON):
        {{
            "quality_issues": ["проблема 1", "проблема 2"],
            "readability_issues": ["проблема 1"],
            "security_issues": [],
            "performance_issues": ["проблема 1"],
            "suggestions": ["предложение 1", "предложение 2"]
        }}
        
        Верни только JSON, без пояснений.
        """
        
        response = self.client.chat(prompt)
        result = response.choices[0].message.content
        
        # Извлечение JSON из ответа
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0]
        elif "```" in result:
            result = result.split("```")[1]
        
        try:
            return json.loads(result.strip())
        except json.JSONDecodeError:
            return {"error": ["Не удалось распарсить ответ"], "raw_response": result}
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Простой чат с GigaChat
        
        Args:
            message: Сообщение пользователя
            system_prompt: Системный промпт (опционально)
            
        Returns:
            Ответ ассистента
        """
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nПользователь: {message}\nАссистент:"
        else:
            full_prompt = message
        
        response = self.client.chat(full_prompt)
        return response.choices[0].message.content


# Пример использования
if __name__ == "__main__":
    assistant = GigaChatAssistant()
    
    # Тестирование чата
    print("=== Тест чата ===")
    response = assistant.chat("Привет! Расскажи, что ты умеешь?")
    #print(f"Ответ: {response}\n")
    
    # TODO: Добавьте остальные тесты
    # TODO: Заполните промпты для генерации
    description_1 = "Напиши функцию validate_email(email: str) -> bool, которая проверяет корректность email-адреса..."
    # Ваш код:

    description_2 = "Напиши функцию sort_by_key(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]..."

    description_3 = "Напиши декоратор timer(func) для измерения времени выполнения функции..."

    #Генерация кода
    assistant = GigaChatAssistant()
    code_1 = assistant.generate_code(description_1)
    code_2 = assistant.generate_code(description_2)
    code_3 = assistant.generate_code(description_3)
    # print('1 запрос')
    # print(code_1)
    # print('2 запрос')
    # print(code_2)
    # print('3 запрос')
    # print(code_3)

    # # TODO: Выполните рефакторинг
    assistant = GigaChatAssistant()
    bad_code = open("bad_code.py").read()

    refactored = assistant.refactor_code(
        bad_code,
        requirements="""
        1. Переименуй функции и переменные в осмысленные имена
        2. Добавь аннотации типов
        3. Добавь docstring для каждой функции
        4. Замени глобальную переменную на константу
        5. Добавь обработку ошибок в get_user
        """
    )

    # print("=== ОТРЕФАКТОРЕННЫЙ КОД ===")
    # print(refactored)


    # TODO: Сгенерируйте тесты для отрефакторенных функций
    tests = assistant.generate_tests(refactored, framework="pytest")
    print("=== СГЕНЕРИРОВАННЫЕ ТЕСТЫ ===")
    print(tests)

    # Сохраните тесты в файл
    # with open("test_refactored.py", "w") as f:
    #     f.write(tests)  

    # Запустите тесты (если pytest установлен)
    # pytest test_refactored.py -v
    # TODO: Проанализируйте сгенерированный код
    code_to_analyze = code_1 + "\n\n" + code_2 + "\n\n" + code_3
    analysis = assistant.analyze_code(code_to_analyze)

    print("=== РЕЗУЛЬТАТЫ АНАЛИЗА ===")
    for category, issues in analysis.items():
        print(f"\n{category.upper()}:")
        for issue in issues:
            print(f"  - {issue}")

    readme = assistant.generate_documentation(code_1 + code_2 + code_3, doc_type="readme")
    print("=== СГЕНЕРИРОВАННАЯ ДОКУМЕНТАЦИЯ ===")
    print(readme)

    # Сохраните README
    with open("README_generated.md", "w") as f:
        f.write(readme)