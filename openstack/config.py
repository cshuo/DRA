from oslo_config import cfg

CONF = cfg.CONF

rpcapi_opts = [
    cfg.StrOpt('selector_topic',
               default='selector_topic',
               help='the topic that selector_topic service listen on'),
    cfg.StrOpt('controller_topic',
               default='controller_topic',
               help='the topic that controller service listen on')
]

CONF.register_opts(rpcapi_opts)
