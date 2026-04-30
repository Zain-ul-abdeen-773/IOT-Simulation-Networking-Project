import time

def inject_java_class():
    with open('OfflineAiPredictor.java', 'r', encoding='utf-8') as f:
        java_code = f.read()

    # Remove the package declaration if it exists
    if java_code.startswith('package '):
        java_code = java_code.split('\n', 1)[1]

    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    if '</JavaClasses>' not in content:
        print("Error: </JavaClasses> tag not found!")
        return

    # Generate a unique ID
    unique_id = str(int(time.time() * 1000))

    java_class_xml = f"""		<JavaClass>
			<Id>{unique_id}</Id>
			<Name><![CDATA[OfflineAiPredictor]]></Name>
			<Text><![CDATA[{java_code.strip()}]]></Text>
		</JavaClass>
"""

    content = content.replace('</JavaClasses>', java_class_xml + '\t</JavaClasses>')

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected OfflineAiPredictor into <JavaClasses> block!")

if __name__ == '__main__':
    inject_java_class()
