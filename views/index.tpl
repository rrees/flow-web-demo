
<h1>Flow chart demo</h1>

<p>This is a demo of how to build a website entirely on top of a graph database</p>

<h2>Available flows</h2>

<ul>
	% for flow in flows:
	<li><a href="/flow/{{flow['id']}}">View flow <q>{{flow['title']}}</q></a> or <a href="/start/flow/{{flow['id']}}">start flow</a</li>
	% end
	
</ul>

%rebase layout title='Introduction'