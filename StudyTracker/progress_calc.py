class ProgressCalculator:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def calculate_subject_completion(self, subject):
        data = self.data_manager.load_data()
        if not data[subject]["topics"]:
            return 0

        total_subtopics = 0
        completed_subtopics = 0

        for topic in data[subject]["topics"].values():
            for subtopic in topic["subtopics"].values():
                total_subtopics += 1
                if subtopic["completed"]:
                    completed_subtopics += 1

        return int((completed_subtopics / total_subtopics * 100) if total_subtopics > 0 else 0)