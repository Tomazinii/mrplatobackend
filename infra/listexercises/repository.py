from interfaces.repository import ExerciseRepositoryInterface

class ExerciseRepository(ExerciseRepositoryInterface):
    """ This is the class to exercise repository """

    @classmethod
    def get_list(self, index_list_exercise: int = None):
        if index_list_exercise:
            list_of_problems = [
                {"text":'1 - p → q , p ⊢ q', "id":0}, 
                {"text":'2 - p → q , ~q ⊢ ~p',"id":1}, 
                {"text":'3 - p → q , q → s ⊢ p → s',"id":2}, 
                {"text":'4 - p , q ⊢ p',"id":3}, 
                {"text":'4 - p , q ⊢ p',"id":4}, 
                {"text": "11 - ~ p -> ~ q , q ⊢ p", "id": 5},
                {"text": "12 - p v q , ~ q , p -> r ^ s ⊢ s ^ r", "id": 6},
                {"text": "13 - (r ^ ~ t ) -> ~ s , p -> s , p ^ q ⊢ ~ ( ~ t ^ r)", "id": 7},
                {"text": "14 - (r ^ s) v p , q -> ~ p , t -> ~ p , q v t ⊢ s ^ r", "id": 8},
                {"text": "15 - ~ p v ~ q , ~ r -> p , r -> ~ s , s ⊢ ~ q", "id": 9},
                {"text": "16 - p -> q v r , ~ ~ p , ~ r ⊢ q", "id": 10},
                {"text": "17 - r -> p ^ ~ q , r v ~ s , s ⊢ ~ q ^ p", "id": 11},
                {"text": "18 - ~ ( p ^ q) , ~ q -> r , ~ p -> r , s -> ~ r ⊢ ~ s", "id": 12},
                {"text": "19 - p ^ ~ q , p -> ~ r , q v ~ s ⊢ ~ ( r v s )", "id": 13},
                {"text": "20 - ~ s -> ~ ( p v ~ t) , t -> q ^ r , ~s ⊢ r ^ q", "id": 14},
                {"text": "21 - ~ p -> q , r -> q , r v ~ p , ~ q v s ⊢ s", "id": 15},
                {"text": "22 - t -> p ^ s , q -> ~ p , r -> ~ s , r v q ⊢ ~ t", "id": 16},
                {"text": "23 - r -> ~ p , (r ^ s) v t , t -> q v u , ~ q ^ ~ u ⊢ ~ p", "id": 17},
                {"text": "24 - p v q , s -> q ^ r , p -> s , q -> s ⊢ r ^ q", "id": 18},
                {"text": "25 - ~ ( p v ~ r ) , p v q , r -> s , q ^ s -> t ^ s ⊢ s ^ t", "id": 19},
                {"text": "26 - p -> q , q -> r ⊢ ~ p v r", "id": 20}
                ]
            return list_of_problems
        list_of_problems = [ "1 - p → q , p ⊢ q",
            "2 - p → q , ~q ⊢ ~p",
            "3 - p → q , q → s ⊢ p → s",
            "4 - p , q ⊢ p",
            "4 - p , q ⊢ p",
            "11 - ~ p -> ~ q , q ⊢ p",
            "12 - p v q , ~ q , p -> r ^ s ⊢ s ^ r",
            "13 - (r ^ ~ t ) -> ~ s , p -> s , p ^ q ⊢ ~ ( ~ t ^ r)",
            "14 - (r ^ s) v p , q -> ~ p , t -> ~ p , q v t ⊢ s ^ r",
            "15 - ~ p v ~ q , ~ r -> p , r -> ~ s , s ⊢ ~ q",
            "16 - p -> q v r , ~ ~ p , ~ r ⊢ q",
            "17 - r -> p ^ ~ q , r v ~ s , s ⊢ ~ q ^ p",
            "18 - ~ ( p ^ q) , ~ q -> r , ~ p -> r , s -> ~ r ⊢ ~ s",
            "19 - p ^ ~ q , p -> ~ r , q v ~ s ⊢ ~ ( r v s )",
            "20 - ~ s -> ~ ( p v ~ t) , t -> q ^ r , ~s ⊢ r ^ q",
            "21 - ~ p -> q , r -> q , r v ~ p , ~ q v s ⊢ s",
            "22 - t -> p ^ s , q -> ~ p , r -> ~ s , r v q ⊢ ~ t",
            "23 - r -> ~ p , (r ^ s) v t , t -> q v u , ~ q ^ ~ u ⊢ ~ p",
            "24 - p v q , s -> q ^ r , p -> s , q -> s ⊢ r ^ q",
            "25 - ~ ( p v ~ r ) , p v q , r -> s , q ^ s -> t ^ s ⊢ s ^ t",
            "26 - p -> q , q -> r ⊢ ~ p v r"
    ]
        return [{"list_of_problems":list_of_problems, "slug":"lista-01", "availability": True, "id":0}]
