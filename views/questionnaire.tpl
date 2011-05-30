
<h1>{{questionnaire['title']}}</h1>

<p>{{questionnaire['description']}}</p>

<h2>Questions in this flow</h2>

<ul>
	% for question in questions:
	<li><a href="/flow/{{questionnaire['id']}}/question/{{question['id']}}">{{question['text']}}</a></li>
	% end
	
</ul>

%rebase layout title='Flow'