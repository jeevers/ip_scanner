<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="/static/style.css" type="text/css" />
	</head>
	<body>
		{% for vlan in ip_usage %}
		<div class="vlan">
			<table>
				<thead>
					<tr>
						<th>IP Address</th>
						<th>State</th>
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
				</tr>
				{% end %}
			</table>
		</div>
		{% end %}
	</body>
</html>
