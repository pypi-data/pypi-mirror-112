ERROR_TYPE = (
    ("VALIDATION_FAILURE", "request parameters validation failed", "请求参数验证失败"),
    ("NO_ACCESS_RIGHT", "no resource access rights", "没有资源访问权限"),
    ("INVALID_TOKEN", "invalid token", "无效API Token"),
    ("UNKNOWN_METRICS", "The target name for the feedback is not defined in the experiment configuration",
     "反馈的目标名称在实验配置中未定义"),
    ("METRICS_COUNT_MISMATCH", "The number of feedback targets does not match the experimental configuration",
     "反馈的目标个数与实验配置不匹配"),
    ("MAX_PARALLEL_TRIALS_REACHED", "The maximum number of parallel attempts has been reached",
     "已达到实验最大尝试并行数"),
    ("EXPERIMENT_NOT_RUNNING", "The experiment has not started, no other operation can be carried out",
     "实验未开始，不能进行其他操作")
)