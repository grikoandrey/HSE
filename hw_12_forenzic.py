import pyshark
import pandas as pd

# показывать все столбцы
pd.set_option('display.max_columns', None)
# показывать все строки
pd.set_option('display.max_rows', None)
# не сокращать содержимое ячеек
pd.set_option('display.max_colwidth', None)
# Не переносить DataFrame на несколько строк
pd.set_option('display.expand_frame_repr', False)

pcap_file = 'dhcp.pcapng'
cap = pyshark.FileCapture(
    pcap_file,
    tshark_path='/Volumes/CORSAIR/Wireshark.app/Contents/MacOS/tshark'
)

dhcp_events = []

for packet in cap:
    if 'DHCP' in packet:
        dhcp_events.append({
            'time': packet.sniff_time,
            'transaction_id': packet.dhcp.id,
            'message_type': packet.dhcp.option_dhcp,
            'client_mac': packet.dhcp.hw_mac_addr,
            'your_ip': getattr(packet.dhcp, 'ip_your', None),
            'server_ip': getattr(packet.dhcp, 'option_dhcp_server_id', None)
        })

dns_events = []

for packet in cap:
    if 'DNS' in packet:
        dns_events.append({
            'time': packet.sniff_time,
            'query_name': getattr(packet.dns, 'qry_name', None),
            'query_type': getattr(packet.dns, 'qry_type', None),
            'src_ip': packet.ip.src if 'IP' in packet else None,
            'dst_ip': packet.ip.dst if 'IP' in packet else None
        })

ip_events = []

for packet in cap:
    if 'IP' in packet:
        ip_events.append({
            'time': packet.sniff_time,
            'src_ip': packet.ip.src,
            'dst_ip': packet.ip.dst,
            'protocol': packet.transport_layer
        })

cap.close()

# DHCP
df_dhcp = pd.DataFrame(dhcp_events)
# Пример для DHCP
df_dhcp['time'] = pd.to_datetime(df_dhcp['time'])

# Форматируем вывод datetime (например, YYYY-MM-DD HH:MM:SS)
df_dhcp['time_str'] = df_dhcp['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
# print(df_dhcp)
print('DHCP события ==============================')
print(df_dhcp[['time_str', 'transaction_id', 'message_type', 'client_mac', 'your_ip', 'server_ip']])
# df_dhcp.to_csv('dhcp_log.csv', index=False)

# DNS
print('DNS события ==============================')
if dns_events is None or len(dns_events) == 0:
    print("DNS events отсутствуют")
    df_dns = pd.DataFrame()
else:
    df_dns = pd.DataFrame(dns_events)
    print(df_dns)
# df_dns.to_csv('dns_log.csv', index=False)

# IP
df_ip = pd.DataFrame(ip_events)
df_ip['time'] = pd.to_datetime(df_ip['time'])
df_ip['time_str'] = df_ip['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
print('IP запросы ==============================')
print(df_ip[['time_str', 'src_ip', 'dst_ip', 'protocol']])
# df_ip.to_csv('ip_log.csv', index=False)
