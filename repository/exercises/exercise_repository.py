from interfaces.repository import ExerciseRepositoryInterface



class ExerciseRepository(ExerciseRepositoryInterface):
    """ This is the class to exercise repository """

    @classmethod
    def get_list(self, index_list_exercise: int = None):
        if index_list_exercise:
            list_of_problems = [{"text":'1 - p → q , p ⊢ q', "id":0}, {"text":'2 - p → q , ~q ⊢ ~p',"id":1}, {"text":'3 - p → q , q → s ⊢ p → s',"id":2}, {"text":'4 - p , q ⊢ p',"id":3}]
            return list_of_problems
        
        list_of_problems = ['1 - p → q , p ⊢ q', '2 - p → q , ~q ⊢ ~p', '3 - p → q , q → s ⊢ p → s', '4 - p , q ⊢ p']
        return [{"list_of_problems":list_of_problems, "slug":"lista-01", "availability": True, "id":0}]
