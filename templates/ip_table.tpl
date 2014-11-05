<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="/static/style.css" type="text/css" />
        <script src="/static/jquery-2.1.1.min.js"></script>
        <script src="/static/ip_table.js"></script>
	</head>
	<body>
        <div id="selections">
            <button type="button" class="dnstoggle">Toggle Name Resolution</button>
            {% for index, subnet in enumerate(ip_usage) %}
               <input type="checkbox" name="subnet" value="{{escape("subnet"+str(index))}}" checked><a href="/#{{escape("subnet"+str(index))}}">{{escape(subnet)}}</a><br>
            {% end %}
        </div>
        <div id='tablecontainer'>
        {% for index, subnet in enumerate(ip_usage) %}
		<div class="vlan" id="{{escape("subnet"+str(index))}}">
			<table>
				<thead>
					<tr>
						<th><a name="{{ escape("subnet"+str(index)) }}">IP Address</a></th>
						<th>State</th>
						<th class="dnsname">DNS Name</th>
					</tr>
				<thead>
				{% for ip in ip_usage[subnet] %}
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
        </div>
	</body>
</html>
