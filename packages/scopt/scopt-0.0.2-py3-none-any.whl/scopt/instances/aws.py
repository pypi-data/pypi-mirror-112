from scopt.instances import Instance


# EMR instance types.
# If you want to add new instance type, check following url to confirm how many
# memory can use for a spark executor.
# yarn.nodemanager.resource.memory-mb is maximum value for one executor.
# https://docs.aws.amazon.com/ja_jp/emr/latest/ReleaseGuide/emr-hadoop-task-config.html
r4_xlarge = Instance(4, 22)
r4_2xlarge = Instance(8, 53)
r4_4xlarge = Instance(16, 114)
r4_8xlarge = Instance(32, 236)
r4_16xlarge = Instance(64, 480)
r5_xlarge = Instance(4, 24)
r5_2xlarge = Instance(8, 56)
r5_4xlarge = Instance(16, 120)
r5_8xlarge = Instance(32, 248)
r5_12xlarge = Instance(48, 376)
r5_16xlarge = Instance(64, 504)
r5_24xlarge = Instance(96, 760)
