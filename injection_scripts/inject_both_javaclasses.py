import time

def inject_java_classes():
    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    if '</JavaClasses>' not in content:
        print("Error: </JavaClasses> tag not found!")
        return

    # 1. Inject OfflineAiPredictor
    with open('model/OfflineAiPredictor.java', 'r', encoding='utf-8') as f:
        java_code_1 = f.read().replace('package finalccnproject;\n\n', '')
    
    # 2. Inject AnomalyModel
    with open('model/AnomalyModel.java', 'r', encoding='utf-8') as f:
        java_code_2 = f.read().replace('package finalccnproject;\n\n', '')

    id_1 = str(int(time.time() * 1000) + 1)
    java_class_xml_1 = f"""		<JavaClass>
			<Id>{id_1}</Id>
			<Name><![CDATA[OfflineAiPredictor]]></Name>
			<Text><![CDATA[{java_code_1.strip()}]]></Text>
		</JavaClass>
"""

    id_2 = str(int(time.time() * 1000) + 2)
    java_class_xml_2 = f"""		<JavaClass>
			<Id>{id_2}</Id>
			<Name><![CDATA[AnomalyModel]]></Name>
			<Text><![CDATA[{java_code_2.strip()}]]></Text>
		</JavaClass>
"""

    # Remove any existing OfflineAiPredictor JavaClass before injecting
    import re
    content = re.sub(r'<JavaClass>\s*<Id>\d+</Id>\s*<Name><!\[CDATA\[OfflineAiPredictor\]\]></Name>.*?</JavaClass>', '', content, flags=re.DOTALL)

    content = content.replace('</JavaClasses>', java_class_xml_1 + java_class_xml_2 + '\t</JavaClasses>')

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected both models into <JavaClasses>!")

if __name__ == '__main__':
    inject_java_classes()
