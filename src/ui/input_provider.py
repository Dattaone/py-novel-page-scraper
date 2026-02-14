from abc import ABC, abstractmethod


class InputProvider(ABC):
    @abstractmethod
    def get_utl(self)->str:
        pass

    @abstractmethod
    def get_filename(self)->str:
        pass

    @abstractmethod
    def get_chapter_range(self)->str:
        pass
        
    @abstractmethod
    def gselect_option(self, prompt, options)->str:
        pass