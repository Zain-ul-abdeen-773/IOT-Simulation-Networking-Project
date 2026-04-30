import time

def inject_forecaster():
    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    if '</JavaClasses>' not in content:
        print("Error: </JavaClasses> tag not found!")
        return

    with open('model/FutureForecaster.java', 'r', encoding='utf-8') as f:
        java_code = f.read().replace('package finalccnproject;\n\n', '')
    
    unique_id = str(int(time.time() * 1000) + 3)
    java_class_xml = f"""		<JavaClass>
			<Id>{unique_id}</Id>
			<Name><![CDATA[FutureForecaster]]></Name>
			<Text><![CDATA[{java_code.strip()}]]></Text>
		</JavaClass>
"""

    import re
    # Remove existing if any
    content = re.sub(r'<JavaClass>\s*<Id>\d+</Id>\s*<Name><!\[CDATA\[FutureForecaster\]\]></Name>.*?</JavaClass>', '', content, flags=re.DOTALL)

    content = content.replace('</JavaClasses>', java_class_xml + '\t</JavaClasses>')

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected FutureForecaster into <JavaClasses>!")

if __name__ == '__main__':
    inject_forecaster()
