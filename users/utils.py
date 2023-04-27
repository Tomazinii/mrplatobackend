from config.models import ConfigRate
from exercises.models import Question

from infra.user.models import Score, UserAccount


def verify_score(type,question_id,user_score):
    score = Score.objects.filter(type=type,user_score=user_score,question_id=question_id)

    if score[0].acert == True or score[0].tried == True:
        return False
    
    return True


def score(type,question_id,user,time,attempet):
    confi_rate = ConfigRate.objects.first()
    rate_challenges =  confi_rate.rate_challenges
    rate_exercise =  confi_rate.rate_exercise
    rate_games =  confi_rate.rate_games
    rate_tournamment =  confi_rate.rate_tournamment

    users = UserAccount.objects.filter(id=user.id)

    if type == "exercises":

        score = Score.objects.filter(type=type,user_score=user,question_id=question_id)

        if score.__len__() != 0:
            if score[0].acert == True or score[0].tried == True:
                print("Ja fez o exercicio")
                return 

  
        for z in users:
            print(rate_exercise)
            z.score_user += rate_exercise
            z.save()
            
        set_score = Score.objects.create(type=type,question_id=question_id,user_score=user,acert=True,tried=True,data={"a":"A"})



    if type == "tournamment":
        score = Score.objects.filter(type=type,user_score=user,question_id=question_id)

        if score.__len__() != 0:
            if score[0].acert == True or score[0].tried == True:
                return 

    
        for z in users:
            z.score_user += rate_tournamment
            z.save()
        set_score = Score.objects.create(type=type,question_id=question_id,user_score=user,acert=True,tried=True,data={"a":"A"})
        



    if type == "games":
        score = Score.objects.filter(type=type,user_score=user,question_id=question_id)

        if score.__len__() != 0:
            if score[0].acert == True or score[0].tried == True:
                print("Ja fez o exercicio Tournamment")
                return 

        print("ainda nao fez Tournamment")
    
        for z in users:
            print(rate_exercise)
            z.score_user += rate_games
            z.save()
        set_score = Score.objects.create(type=type,question_id=question_id,user_score=user,acert=True,tried=True,data={"a":"A"})



    if type == "challenges":
        score = Score.objects.filter(type=type,user_score=user,question_id=question_id)

        if score.__len__() != 0:
            if score[0].acert == True or score[0].tried == True:
                print("Ja fez o exercicio Tournamment")
                return 

        print("ainda nao fez Tournamment")
    
        for z in users:
            print(rate_exercise)
            z.score_user += rate_challenges
            z.save()
        set_score = Score.objects.create(type=type,question_id=question_id,user_score=user,acert=True,tried=True,data={"a":"A"})