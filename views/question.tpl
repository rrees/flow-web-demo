
<h1>{{flow['title']}}</h1>

<h2>{{question['text']}}</h2>


% for answer in answers:
<li><a href="/flow/{{flow['id']}}/question/{{question['id']}}/answer/{{answer['id']}}">{{answer['text']}}</a></li>


%rebase layout title='Question'