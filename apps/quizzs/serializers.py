from rest_framework import serializers
from .models import Question, QuestionChoice, Quiz, QuizUser, Category

class ChoiceAutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ['id', 'is_true', 'content']       #the autor can see the response

class ChoicePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ['id', 'content']          #is_true is not known so he can't have the response

class QuestionAuthorSerializer(serializers.ModelSerializer):
    choices = ChoiceAutorSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'explanation', 'quiz']

class QuestionPlayerSerializer(serializers.ModelSerializer):    #We suppose player being autor right after he responses question
    choices = ChoicePlayerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'quiz']

class QuizCreateSerializer(serializers.ModelSerializer):
    questions = QuestionAuthorSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "difficulty", "is_public", "category", "questions"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")        #Go out questions for set quiz with title, etc ...
        quiz = Quiz.objects.create(**validated_data)    #"**"" is for use unpack python dictionary to set all value to create the quiz.

        for question_data in questions_data:
            choices_data = questions_data.pop("choices")
            question = Question.objects.create(quiz=quiz, **question_data)

            for choice_data in choices_data:
                QuestionChoice.objects.create(question=question, **choice_data)

        return quiz