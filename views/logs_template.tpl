<table>
	<thead><tr><th>Host ID</th><th>CPU usage(%)</th></tr></thead>
	<tbody>
%for item in logs:
  <tr><td>{{item["hostId"]}}</td><td>{{item["cpu"]}}</td></tr>
%end
	</tbody>
</table>