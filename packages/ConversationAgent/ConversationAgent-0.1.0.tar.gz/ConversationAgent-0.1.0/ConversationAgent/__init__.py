import json
import uuid
import re

__USER_TEXT__ = "USER_TEXT"
__PASS_TOKEN__ = "PASS_TOKEN"
__SYS_REPLY__ = "SYS_REPLY"
__SYS_STAGE__ = "SYS_STAGE"
__KEEP_VAR__ = "KEEP_VAR"
__KEEP_DEFAULT_VAR__ = "KEEP_DEFAULT_VAR"
__LOCAL_VAR_LABEL__ = "__LOCAL_VAR_LABEL__"
__LOCAL_VAR_VALUE__ = "__LOCAL_VAR_VALUE__"
__MOCK_SATGES_LABEL_1__ = "__MOCK_SATGES_LABEL_1__"

class StageStatus:
    INIT = "INIT"
    FIRST = "FIRST"
    REFUSE = "REFUSE"
    COMPLETE = "COMPLETE"


class StageType:
    BASE = "BASE"
    SWITCH = "Switch"


class Stage:
    def __init__(self, **kwargs):
        self.stage_type = StageType.BASE
        self.stage_id = f"{self.stage_type}:{str(uuid.uuid4())[:15]}"
        self.data = kwargs
        self.sys_reply_q1 = "init sys reply" #init
        self.sys_reply_q2 = "refuse sys reply" #refuse
        self.sys_reply_complete = "complete sys reply" #complete

    @staticmethod
    def set_sys_stage_status(data: dict, label: str) -> dict:
        data.update({__SYS_STAGE__: label})
        return data

    @staticmethod
    def get_sys_stage_status(data: dict) -> str:
        return data.get(__SYS_STAGE__, None)

    @staticmethod
    def is_first_access(data, stage_id):
        # First Access
        if __PASS_TOKEN__ not in data:
            return True
        if stage_id not in data[__PASS_TOKEN__]:
            return True
        return False

    @staticmethod
    def clear_user_text(data):
        # First Access
        _ = data.pop(__USER_TEXT__, None)
        return data

    @classmethod
    def save_user_text(cls, data, stage_id, label):
        user_text = cls.get_user_text(data)
        return cls.set_var(data, stage_id, label, user_text)

    @staticmethod
    def get_user_text(data):
        return data.get(__USER_TEXT__, None)

    @staticmethod
    def is_token_pass(data: dict, stage_id) -> bool:
        token = data.get(__PASS_TOKEN__, None)
        if token is None:
            return False
        if isinstance(token, dict) and token.get(stage_id, None) is True:
            return True
        else:
            return False

    @staticmethod
    def set_none_token_pass(data, stage_id):
        if __PASS_TOKEN__ not in data:
            data[__PASS_TOKEN__]={}
        data[__PASS_TOKEN__][stage_id] = None
        return data

    @staticmethod
    def set_true_token_pass(data, stage_id):
        if __PASS_TOKEN__ not in data:
            data[__PASS_TOKEN__] = {}
        data[__PASS_TOKEN__][stage_id] = True
        return data

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        kwargs = self.set_default_var(kwargs, __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__)
        # if want to reset data, return (True,None) to replace to (True,kwargs)
        return True, kwargs

    @staticmethod
    def is_var_label(label_string):
        return None if re.match("^var\t.*\t.*\tvar$", label_string) is None else label_string.split("\t")

    @staticmethod
    def is_var_label_human(label_string):
        return None if re.match("^%%.*%%$", label_string) is None else label_string[2:-2]

    @classmethod
    def get_default_var_label(cls, label: str):
        return cls.get_var_label(__KEEP_DEFAULT_VAR__, label)

    def set_default_var(self, data, label, save_text):
        data = self.set_var(data, self.stage_id, label, save_text)
        return self.set_var(data, __KEEP_DEFAULT_VAR__, label, save_text)

    def get_default_var(self, data, label):
        return self.get_var(data, __KEEP_DEFAULT_VAR__, label)

    @staticmethod
    def get_var_label(stage_id: str, label: str):
        assert "\t" not in stage_id
        assert "\t" not in label
        return f"var\t{stage_id}\t{label}\tvar"

    @classmethod
    def set_var(cls, data, stage_id, label, save_text):
        if __KEEP_VAR__ not in data:
            data[__KEEP_VAR__] = {}
        if stage_id not in data[__KEEP_VAR__]:
            data[__KEEP_VAR__][stage_id] = {}

        data[__KEEP_VAR__][stage_id][label] = save_text
        return data

    @classmethod
    def get_var(cls, data, stage_id, label):
        try:
            return data[__KEEP_VAR__][stage_id][label]
        except KeyError:
            return None

    @staticmethod
    def set_sys_reply(data, sys_reply_text):
        if __SYS_REPLY__ in data:
            data[__SYS_REPLY__].append(sys_reply_text)
        else:
            data[__SYS_REPLY__] = [sys_reply_text]
        return data


    @classmethod
    def replace_var_ticket_to_string(cls, kwargs, sys_reply):
        #print(f"kwargs: {kwargs}")
        #print(f"sys_reply: {sys_reply}")
        __NEXT_LINE__ = "||n||"
        # insert ENTITY
        sys_reply_complete_refactor = ""
        ##
        sys_reply = sys_reply.replace("\n", __NEXT_LINE__)

        #
        for var in sys_reply.split(" "):

            # parse
            var_ticket_human = cls.is_var_label_human(var)
            if var_ticket_human is not None:
                var_ticket = cls.get_default_var_label(var_ticket_human).split("\t")
            else:
                var_ticket = cls.is_var_label(var)

            # replace
            if var_ticket is not None:
                try:
                    var_value = kwargs[__KEEP_VAR__][var_ticket[1]][var_ticket[2]]
                    if isinstance(var_value, str):
                        sys_reply_complete_refactor += var_value
                    elif isinstance(var_value, float):
                        sys_reply_complete_refactor += str(round(var_value, 4))
                    else:
                        sys_reply_complete_refactor += str(var_value)

                except KeyError:
                    sys_reply_complete_refactor += var
            else:
                var = var.replace(__NEXT_LINE__, "\n")
                sys_reply_complete_refactor += var
        return sys_reply_complete_refactor

    def run(self, **kwargs):
        if self.is_token_pass(data=kwargs, stage_id=self.stage_id) is True:
            kwargs = self.set_sys_stage_status(kwargs, StageStatus.COMPLETE)
            return kwargs

        if self.is_first_access(kwargs, self.stage_id) is True:
            kwargs = self.set_none_token_pass(data=kwargs, stage_id=self.stage_id)
            kwargs = self.set_sys_stage_status(kwargs, StageStatus.FIRST)
            sys_reply = self.replace_var_ticket_to_string(kwargs, self.sys_reply_q1)
            return self.set_sys_reply(kwargs, sys_reply)

        is_fit_token, kwargs = self.is_fit_needs_n_gen_entity(kwargs)
        if is_fit_token is False:  # q1
            kwargs = self.set_sys_stage_status(kwargs, StageStatus.REFUSE)
            sys_reply = self.replace_var_ticket_to_string(kwargs, self.sys_reply_q2)
            return self.set_sys_reply(kwargs, sys_reply)

        elif is_fit_token is True and kwargs is not None:  # q2
            kwargs = self.save_user_text(kwargs, self.stage_id, __USER_TEXT__)
            kwargs = self.clear_user_text(kwargs)
            kwargs = self.set_true_token_pass(kwargs, stage_id=self.stage_id)
            kwargs = self.set_sys_stage_status(kwargs, StageStatus.COMPLETE)

            # insert ENTITY
            sys_reply = self.replace_var_ticket_to_string(kwargs, self.sys_reply_complete)
            return self.set_sys_reply(kwargs, sys_reply)

        elif is_fit_token is True and kwargs is None:  # reset route
            sys_reply = self.replace_var_ticket_to_string(kwargs, self.sys_reply_complete)
            return self.set_sys_reply({}, sys_reply)


a = Stage()
res = a.run()
assert res.get(__SYS_STAGE__, None) == StageStatus.FIRST
res[__USER_TEXT__] = "hi"
res.pop(__SYS_REPLY__)
res = a.run(**res)
assert res.get(__SYS_STAGE__, None) == StageStatus.COMPLETE
res.pop(__SYS_REPLY__)
res = a.run(**res)
assert res.get(__SYS_STAGE__, None) == StageStatus.COMPLETE


class SwitchStage(Stage):

    def __init__(self,stages_filter):
        super(SwitchStage, self).__init__()
        self.stage_type = StageType.SWITCH
        self.stages_filter = stages_filter


    @staticmethod
    def is_first_access(data, stage_id):
        return False

    def find_new_stages(self, kwargs):

        print(f"filter_tuple: {self.stages_filter}")
        for filter_tuple in self.stages_filter:
            print(f"filter_tuple: {filter_tuple}")
            label, text, stages_label = filter_tuple
            try:
                if self.get_default_var(kwargs, label) == text:
                    return stages_label
            except KeyError as e:
                print(e)
        raise RuntimeError

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        raise RuntimeError("Not support run method, Please use `MultiAgent` to replace `Agent`")


class Agent:
    final_saying = "thanks for using."

    def __init__(self, stages: [Stage]):
        self.stages = stages
        self.final_saying = "thanks for using."

    @staticmethod
    def is_ready_to_reply(data) -> bool:
        status = Stage.get_sys_stage_status(data)
        return True if status in [StageStatus.FIRST,StageStatus.REFUSE] else False

    @staticmethod
    def is_final_stage(stages, idx) -> bool:
        return True if len(stages) == (idx+1) else False

    @staticmethod
    def clear_sys_reply(data):
        data.pop(__SYS_REPLY__,None)
        return data
    @classmethod
    def get_sys_reply(cls, data):
        reply: list = data.get(__SYS_REPLY__, [])
        if cls.is_ready_to_reply(data) is False:
            reply.append(cls.final_saying)
        return reply

    def run_all_stages(self, **kwargs) -> (list, dict):
        #
        kwargs = self.clear_sys_reply(kwargs)

        #
        for idx, stage in enumerate(self.stages):
            #print(f"kwargs in: {kwargs}")
            kwargs = stage.run(**kwargs)
            if self.is_ready_to_reply(kwargs) is True:
                #print(f"\tkwargs out: {kwargs}")
                return self.get_sys_reply(kwargs), kwargs
            else:
                if self.is_final_stage(self.stages, idx) is True:
                    #print(f"\tkwargs out: {kwargs}")
                    return self.get_sys_reply(kwargs), kwargs

        raise RuntimeError


class MultiAgent(Agent):
    __MAIN_STAGES__ = "__MAIN_STAGES__"
    __MAX_LEVEL__ = 10

    def __init__(self, stages: dict):
        assert self.__MAIN_STAGES__ in stages, "__MAIN_STAGES__ need in stages"
        super().__init__(stages[self.__MAIN_STAGES__])
        self.multi_stages = stages
        self.__STAGES_IDS__ = []

    def to_dict(self):
        re_dict = {}
        for key, stages in self.multi_stages.items():
            re_dict[key] = [s.raw_data for s in stages]
        return re_dict

    @staticmethod
    def is_normal_reply(result):
        for r in result:
            if not isinstance(r,str):
                return False
        return True

    @staticmethod
    def is_switch_stage(stage: Stage):
        #print(f"stage:{stage}")
        #print(f"stage:{stage.stage_type}")
        return True if stage.stage_type == StageType.SWITCH else False

    def run_one_stages(self, stages, kwargs):
        #
        # kwargs = self.clear_sys_reply(kwargs)
        #
        for idx, stage in enumerate(stages):
            if stage.stage_id in self.__STAGES_IDS__:
                for rm_idx in self.__STAGES_IDS__[self.__STAGES_IDS__.index(stage.stage_id):]:
                    if rm_idx in kwargs[__PASS_TOKEN__]:
                        del kwargs[__PASS_TOKEN__][rm_idx]
                    if rm_idx in kwargs[__KEEP_VAR__]:
                        for var_name in kwargs[__KEEP_VAR__][rm_idx]:
                            if var_name in kwargs[__KEEP_VAR__][__KEEP_DEFAULT_VAR__]:
                                del kwargs[__KEEP_VAR__][__KEEP_DEFAULT_VAR__][var_name]
                        del kwargs[__KEEP_VAR__][rm_idx]
            self.__STAGES_IDS__.append(stage.stage_id)

            ##
            if self.is_switch_stage(stage) is True:
                stage: SwitchStage
                new_stages_label = stage.find_new_stages(kwargs)
                return self.multi_stages[new_stages_label], kwargs
            else:
                kwargs = stage.run(**kwargs)
                if self.is_ready_to_reply(kwargs) is True:
                    return self.get_sys_reply(kwargs), kwargs
                else:
                    if self.is_final_stage(stages, idx) is True:
                        return self.get_sys_reply(kwargs), kwargs

    def run_all_stages(self, **kwargs) -> (list, dict):
        loop_level = 0
        self.__STAGES_IDS__ = []
        result, kwargs = self.run_one_stages(self.stages, kwargs)
        kwargs = self.clear_sys_reply(kwargs)
        while self.__MAX_LEVEL__ > loop_level:
            loop_level += 1
            if self.is_normal_reply(result):
                return result, kwargs
            else:
                result, kwargs = self.run_one_stages(result, kwargs)




stage1 = Stage()
stage1.sys_reply_q1 = "s1_q1"
stage1.sys_reply_complete = "s1_complete"
stage2 = Stage()
stage2.sys_reply_q1 = "s2_q1"
stage2.sys_reply_complete = "s2_complete"


def mock_client_with_test(agent, says, tests):
    data = {}
    for s, t in zip(says, tests):
        data[__USER_TEXT__] = s
        reply_text, data = agent.run_all_stages(**data)
        assert t == reply_text


def mock_client(agent, says,show_data=True,show_user_text=True):
    data = {}
    for s in says:
        data[__USER_TEXT__] = s
        reply_text, data = agent.run_all_stages(**data)
        if show_user_text:
            print("\t用戶:", s)
        print("系統:", reply_text)
        if show_data:
            print("\t系統資料:", data)


def mock_client_human(agent):
    data = {}
    while True:
        s = input("請輸入：")
        data[__USER_TEXT__] = s
        if s == "exit":
            break
        reply_text, data = agent.run_all_stages(**data)
        print("系統:", reply_text)


def mock_client_once(agent: Agent, text: str, data:dict):
    data[__USER_TEXT__] = text
    return agent.run_all_stages(**data)




mock_client_with_test(Agent([stage1, stage2]), ["hi1", "hi2", "hi3", "hi4", "hi5"],
                      [
                          ['s1_q1'],
                          ['s1_complete', 's2_q1'],
                          ['s2_complete', 'thanks for using.'],
                          ['thanks for using.'],
                          ['thanks for using.']
                      ])

# switch_stage = SwitchStage()
# mock_client_with_test(MultiAgent({
#     MultiAgent.__MAIN_STAGES__: [stage1, stage2, switch_stage],
#     "test": [stage1, stage2],
#     }),
#     ["hi1", "hi2", "hi3", "hi4", "hi5"],
#   [
#       ['s1_q1'],
#       ['s1_complete', 's2_q1'],
#       ['s2_complete', 'thanks for using.'],
#       ['thanks for using.'],
#       ['thanks for using.']
#   ])

stage3 = Stage()
stage3.sys_reply_q1 = "s3_q1"
stage3.sys_reply_complete = "s3_complete"
stage4 = Stage()
stage4.sys_reply_q1 = "s4_q1"
stage4.sys_reply_complete = "s4_complete"
switch_stage = SwitchStage(stages_filter=[
            (__LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__, __MOCK_SATGES_LABEL_1__),
        ])
# mock_client_human(MultiAgent({
#     MultiAgent.__MAIN_STAGES__: [stage1, stage2, switch_stage],
#     __MOCK_SATGES_LABEL_1__: [stage3, stage4],
#     }))