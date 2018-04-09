class subsystem:
    role = ['integration',
            'cdh',
            'power',
            'comms',
            'payload',
            'adcs']

    article = ['flight',
               'engineering',
               'envtest']

    assign = {'role': role,
              'article': article}


class channel:
    protocol = ['uart',
                'i2c',
                'spi',
                '1wire',
                'can',
                'rs23']

    assign = {'protocol': protocol}


class pin:
    function = ['gpio',
            'communication',
            'power',
            'ground']

    direction = ['in',
                 'out',
                 'i/o']

    assign = {'function': function, 'direction': direction}


enums = {'subsystem': subsystem(),
         'channel': channel(),
         'pin': pin()}
