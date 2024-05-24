class FundoInvestimento:
    def __init__(self, TP_FUNDO, CNPJ_FUNDO, DT_COMPTC, VL_TOTAL, VL_QUOTA, VL_PATRIM_LIQ, CAPTC_DIA, RESG_DIA, NR_COTST):
        self.TP_FUNDO = TP_FUNDO
        self.CNPJ_FUNDO = CNPJ_FUNDO
        self.DT_COMPTC = DT_COMPTC
        self.VL_TOTAL = VL_TOTAL
        self.VL_QUOTA = VL_QUOTA
        self.VL_PATRIM_LIQ = VL_PATRIM_LIQ
        self.CAPTC_DIA = CAPTC_DIA
        self.RESG_DIA = RESG_DIA
        self.NR_COTST = NR_COTST
        
    def to_dict(self):
            return {
                'TP_FUNDO': self.TP_FUNDO,
                'CNPJ_FUNDO': self.CNPJ_FUNDO,
                'DT_COMPTC': self.DT_COMPTC,
                'VL_TOTAL': self.VL_TOTAL,
                'VL_QUOTA': self.VL_QUOTA,
                'VL_PATRIM_LIQ': self.VL_PATRIM_LIQ,
                'CAPTC_DIA': self.CAPTC_DIA,
                'RESG_DIA': self.RESG_DIA,
                'NR_COTST': self.NR_COTST
            }        