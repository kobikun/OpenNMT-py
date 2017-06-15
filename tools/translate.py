from __future__ import division

import onmt
import onmt.Markdown
import torch
import argparse
import math

class Option(object):
    def __init__(self):
        self.model = ""
        self.src = ""
        self.src_img_dir = ""
        self.tgt = ""
        self.output = ""
        self.beam_size = 5
        self.batch_size = 30
        self.max_sent_length = 100
        self.replace_unk = False
        self.verbose = False
        self.dump_beam = ""
        self.n_best = 1
        self.gpu = -1
        self.cuda = False

def online_trans_init(opt):
    opt.cuda = opt.gpu > -1
    if opt.cuda:
        torch.cuda.set_device(opt.gpu)
    translator = onmt.Translator(opt)
    return translator

def online_translate(translator, tokenzier, input):
    srcBatch, tgtBatch = [], []
    srcTokens = input.split()
    srcBatch += [srcTokens]
    predBatch, predScore, goldScore = translator.translate(srcBatch, tgtBatch)
    predToken = predBatch[0][0]

    print predBatch
    print predToken
    print " ".join(predToken)

def main(options):
    opt = Option()
    opt.model = options.model
    opt.gpu = options.gpu
    opt.src = options.src

    trans = online_trans_init(opt)

    with open(opt.src, 'rt') as fh:
        for text in fh:
            text = text.rstrip()
            online_translate(trans, None, text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='translate.py')
    onmt.Markdown.add_md_help_argument(parser)

    parser.add_argument('-model', required=True,
                        help='Path to model .pt file')
    parser.add_argument('-src',   required=True,
                        help='Source sequence to decode (one line per sequence)')
    parser.add_argument('-src_img_dir',   default="",
                        help='Source image directory')
    parser.add_argument('-tgt',
                        help='True target sequence (optional)')
    parser.add_argument('-output', default='pred.txt',
                        help="""Path to output the predictions (each line will
                        be the decoded sequence""")
    parser.add_argument('-beam_size',  type=int, default=5,
                        help='Beam size')
    parser.add_argument('-batch_size', type=int, default=30,
                        help='Batch size')
    parser.add_argument('-max_sent_length', type=int, default=100,
                        help='Maximum sentence length.')
    parser.add_argument('-replace_unk', action="store_true",
                        help="""Replace the generated UNK tokens with the source
                        token that had highest attention weight. If phrase_table
                        is provided, it will lookup the identified source token and
                        give the corresponding target token. If it is not provided
                        (or the identified source token does not exist in the
                        table) then it will copy the source token""")
    # parser.add_argument('-phrase_table',
    #                     help="""Path to source-target dictionary to replace UNK
    #                     tokens. See README.md for the format of this file.""")
    parser.add_argument('-verbose', action="store_true",
                        help='Print scores and predictions for each sentence')
    parser.add_argument('-dump_beam', type=str, default="",
                        help='File to dump beam information to.')

    parser.add_argument('-n_best', type=int, default=1,
                        help="""If verbose is set, will output the n_best
                        decoded sentences""")

    parser.add_argument('-gpu', type=int, default=-1,
                        help="Device to run on")

    options = parser.parse_args()
    main(options)
