
<h1>{{flow['title']}}</h1>

<h2>{{question['text']}}</h2>

<ul>
% for answer in answers:
<li><a href="/flow/{{flow['id']}}/question/{{question['id']}}/answer/{{answer['id']}}">{{answer['text']}}</a></li>
%end
</ul>

%rebase layout title='Question'