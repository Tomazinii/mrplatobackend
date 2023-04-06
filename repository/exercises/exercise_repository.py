from interfaces.repository import ExerciseRepositoryInterface



class ExerciseRepository(ExerciseRepositoryInterface):
    """ This is the class to exercise repository """

    @classmethod
    def get_list(self, index_list_exercise: int):
        list_of_problems = ['1 - p → q , p ⊢ q', '2 - p → q , ~q ⊢ ~p', '3 - p → q , q → s ⊢ p → s', '4 - p , q ⊢ p']
        return list_of_problems
