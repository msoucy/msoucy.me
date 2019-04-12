---
Title: Mental Health Quiz
Category: life
...

Below is a mental health quiz that I took at one point.
Fill in the answers based on the following:

- 1 means "Rarely Applies"
- 5 means "Consistently Applies"

<div id="quizbody">
</div>
<input id="grade-button" type="button" onclick="grade()" value="Grade" />
<input id="quiz-reset" type="button" onclick="reset()" value="Reset" />

<div id="results">
  <p>Self Kindness: <input id="result-selfkindness" readonly value="???"/></p>
  <p>Self Judgement: <input id="result-selfjudgement" readonly value="???"/></p>
  <p>Common Humanity: <input id="result-commonhumanity" readonly value="???"/></p>
  <p>Isolation: <input id="result-isolation" readonly value="???"/></p>
  <p>Mindfulness: <input id="result-mindfulness" readonly value="???"/></p>
  <p>Over Identified: <input id="result-overidentified" readonly value="???"/></p>
  <p>Total: <input id="result-total" readonly value="???"/></p>
</div>

<script>
    var questions = [
      "I'm disapproving and judgemental about my own flaws and inadequacies.",
      "When I'm feeling down I tend to obsess and fixate on everything that's wrong",
      "When things are going badly for me, I see the difficulties as part of life that everyone goes through.",
      "When I think about my inadequacies, it tends to make me feel more separate and cut off from the rest of the world.",
      "I try to be loving towards myself when I'm feeling emotional pain.",
      "When I fail at something important to me I become consumed by feelings of inadequacy.",
      "When I'm down and out, I remind myself that there are lots of other people in the world feeling like I am.",
      "When times are really difficult, I tend to be tough on myself.",
      "When something upsets me I try to keep my emotions in balance.",
      "When I feel inadequate in some way, I try to remind myself that feelings of inadequacy are shared by most people.",
      "I'm intolerant and impatient towards those aspects of my personality I don't like.",
      "When I'm going through a very hard time, I give myself the caring and tenderness I need.",
      "When I'm feeling down, I tend to feel like most other people are probably happier than I am.",
      "When something painful happens I try to take a balanced view of the situation.",
      "I try to see my failings as part of the human condition.",
      "When I see aspects of myself that I don't like, I get down on myself.",
      "When I fail at something important to me I try to keep things in perspective.",
      "When I'm really struggling, I tend to feel like other people must be having an easier time of it.",
      "I'm kind to myself when I'm experiencing suffering.",
      "When something upsets me I get carried away with my feelings.",
      "I can be a bit cold-hearted towards myself when I'm experiencing suffering.",
      "When I'm feeling down I try to approach my feelings with curiosity and openness",
      "I'm tolerant of my own flaws and inadequacies.",
      "When something painful happens I tend to blow the incident out of proportion.",
      "When I fail at something that's important to me, I tend to feel alone in my failure.",
      "I try to be understanding and patient towards those aspects of my personality I don't like."
    ]
    onload = function() {
        var quizBody = document.getElementById("quizbody")
        quizbody.innerHtml = ""
        var idx = 1
        questions.forEach(function(el) {
            var selector = document.createElement("input")
            selector.setAttribute("type", "number")
            selector.setAttribute("max", "5")
            selector.setAttribute("min", "1")
            selector.setAttribute("value", "3")
            selector.setAttribute("id", "quiz-question-" + idx)
            quizBody.appendChild(selector)
            quizBody.appendChild(document.createTextNode(idx + ": " + el))
            quizBody.appendChild(document.createElement("br"))
            idx++
        })
    }
    reset = function() {
        var idx = 1
        questions.forEach(function(el) {
            var selector = document.getElementById("quiz-question-" + idx)
            selector.value = "3"
            idx++
        })
    }
    sum_scores = function(qns) {
        var total_score = 0
        var num_qns = 0
        qns.forEach(function(num) {
            total_score += parseInt(document.getElementById("quiz-question-" + num).value)
            num_qns++
        })
        return (total_score/num_qns)
    }
    sum_scores_inv = function(qns) {
        var total_score = 0
        var num_qns = 0
        qns.forEach(function(num) {
            total_score += 6 - parseInt(document.getElementById("quiz-question-" + num).value)
            num_qns++
        })
        return (total_score/num_qns)
    }
    set_result = function(name, tag, score) {
        var elem = document.getElementById("result-" + tag)
        elem.value = score
    }
    grade = function() {
        var selfkindness = sum_scores([5,12,19,23,26])
        set_result("Self Kindness", "selfkindness", selfkindness)
        var selfjudgement = sum_scores_inv([1,8,11,16,21])
        set_result("Self Judgement", "selfjudgement", selfjudgement)
        var commonhumanity = sum_scores([3,7,10,15])
        set_result("Common Humanity", "commonhumanity", commonhumanity)
        var isolation = sum_scores_inv([4,13,18,25])
        set_result("Isolation", "isolation", isolation)
        var mindfulness = sum_scores([9,14,17,22])
        set_result("Mindfulness", "mindfulness", mindfulness)
        var overidentified = sum_scores_inv([2,6,20,24])
        set_result("Over Identified", "overidentified", overidentified)
        var totalScore = (selfkindness + selfjudgement + commonhumanity + isolation + mindfulness + overidentified) / 6
        set_result("Total", "total", totalScore)
    }
</script>
