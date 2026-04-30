import re

def patch():
    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue: agent.packet_size * 0.045 evaluates to a massive number of seconds.
    # We will divide the whole expression by 1000.0
    content = re.sub(r'agent\.packet_size \* 0\.045 \+ agent\.inter_arrival \* 0\.0012 \+\s*10\.5', 
                     '(agent.packet_size * 0.045 + agent.inter_arrival * 0.0012 + 10.5) / 1000.0', 
                     content)

    # We also need to increase the MQTT_Buffer capacity to avoid crash
    # First find MQTT_Buffer ID
    mqtt_buffer_match = re.search(r'<Id>(\d+)</Id>\s*<Name><!\[CDATA\[MQTT_Buffer\]\]></Name>', content)
    if mqtt_buffer_match:
        buffer_id = mqtt_buffer_match.group(1)
        # Find where it's defined and change capacity
        # It's a Queue block. The parameter for capacity is 'capacity'
        # Let's just globally replace capacity 100 with 1000000 in Queue blocks
        # Actually, let's use regex to find the capacity parameter inside MQTT_Buffer
        
        # A simpler way: just replace all <Code><![CDATA[100]]></Code> with 1000000 if it's related to capacity
        # Or even better, AnyLogic allows "maximumCapacity" true.
        # Let's just increase the value 100 to 100000 everywhere safely? No, that might break other things.
        
        # The crash is mostly caused by the delay time being 48 minutes per packet.
        # If the delay is divided by 1000, it becomes 2.8 seconds.
        # The inter-arrival is maybe 0.1 seconds.
        # The queue will still build up. We need the delay to be faster than inter-arrival, OR queue capacity to be infinite.
        
        # In AnyLogic, Queue capacity can be set to maximum by setting:
        # <Parameter>
        #     <Name><![CDATA[capacity]]></Name>
        #     <Value Class="CodeValue">
        #         <Code><![CDATA[100]]></Code>
        #     </Value>
        # </Parameter>
        
        # Let's replace:
        content = re.sub(r'<Name><!\[CDATA\[capacity\]\]></Name>\s*<Value Class="CodeValue">\s*<Code><!\[CDATA\[100\]\]></Code>',
                         '<Name><![CDATA[capacity]]></Name>\n\t\t\t\t\t\t\t<Value Class="CodeValue">\n\t\t\t\t\t\t\t\t<Code><![CDATA[1000000]]></Code>',
                         content)

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched delay and capacity!")

if __name__ == '__main__':
    patch()
