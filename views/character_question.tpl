
<h1>{{character['id']}}</h1>

<p>{{current_question['text']}}</p>

<form method="POST">
	% for answer in answers:
		<p><input type="radio" name="answer" value="{{answer['id']}}"> {{answer['text']}}</p>
	% end
	<p><button type="submit">Answer</button></p>
</form>

%rebase layout title='Character'