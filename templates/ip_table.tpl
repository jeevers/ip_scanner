<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="/static/style.css" type="text/css" />
        <script src="/static/jquery-2.1.1.min.js"></script>
        <script src="/static/ip_table.js"></script>
	</head>
	<body>
        <div class="selections">
            <button type="button" class="dnstoggle">Toggle Name Resolution</button>
        </div>
		{% for vlan in ip_usage %}
		<div class="vlan">
			<table>
				<thead>
					<tr>
						<th>IP Address</th>
						<th>State</th>
						<th class="dnsname">DNS Name</th>
					</tr>
				<thead>
				{% for ip in vlan %}
				<tr>
					<td>{{ escape(ip[0]) }}</td>
					{% if ip[1] == 'ACTIVE' %}
					<td class="active">
					{% else %}
					<td class="inactive">
					{% end %}
					{{ escape(ip[1]) }}
					</td>
                    <td class="dnsname">
                    {{ escape(ip[2]) }}
                    </td>
				</tr>
				{% end %}
			</table>
		</div>
		{% end %}
	</body>
</html>
