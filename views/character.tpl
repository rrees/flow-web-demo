

<h1>{{character['id']}}</h1>

<dl>
	% for attribute in attributes:
	<dt>{{attribute['type']}}</dt>
	<dd>{{attribute['value']}}</dd>
	% end
</dl>
%rebase layout title='Character'