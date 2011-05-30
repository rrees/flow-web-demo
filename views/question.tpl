
<h1>{{flow['title']}}</h1>

<h2>{{question['text']}}</h2>

<ul>
	% for answer in answers:
	<li>{{answer['text']}}</li>
	% end
	
</ul>

%rebase layout title='Question'