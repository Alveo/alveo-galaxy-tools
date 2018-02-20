# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""TensorFlow NMT model implementation."""
from __future__ import print_function

import argparse
import os
import random
import sys


# import matplotlib.image as mpimg
import numpy as np
import tensorflow as tf
import inference
import train
import evaluation_utils
import misc_utils as utils
import vocab_utils

#utils.check_tensorflow_version()

FLAGS = None
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def add_arguments(parser):
  """Build ArgumentParser."""
  parser.register("type", "bool", lambda v: v.lower() == "true")

  # network
  parser.add_argument("--num_units", type=int, default=32, help="Network size.")
  parser.add_argument("--num_layers", type=int, default=6, help="Network depth.")
  parser.add_argument("--encoder_type", type=str, default="uni", help="""\
      uni | bi | gnmt. For bi, we build num_layers/2 bi-directional layers.For
      gnmt, we build 1 bi-directional layer, and (num_layers - 1) uni-
      directional layers.\
      """)
  parser.add_argument("--residual", type="bool", nargs="?", const=True,
                      default=False,
                      help="Whether to add residual connections.")
  parser.add_argument("--time_major", type="bool", nargs="?", const=True,
                      default=True,
                      help="Whether to use time-major mode for dynamic RNN.")
  parser.add_argument("--num_embeddings_partitions", type=int, default=0,
                      help="Number of partitions for embedding vars.")

  # attention mechanisms
  parser.add_argument("--attention", type=str, default="scaled_luong", help="""\
      luong | scaled_luong | bahdanau | normed_bahdanau or set to "" for no
      attention\
      """)
  parser.add_argument(
      "--attention_architecture",
      type=str,
      default="standard",
      help="""\
      standard | gnmt | gnmt_v2.
      standard: use top layer to compute attention.
      gnmt: GNMT style of computing attention, use previous bottom layer to
          compute attention.
      gnmt_v2: similar to gnmt, but use current bottom layer to compute
          attention.\
      """)
  parser.add_argument(
      "--output_attention", type="bool", nargs="?", const=True,
      default=True,
      help="""\
      Only used in standard attention_architecture. Whether use attention as
      the cell output at each timestep.
      .\
      """)
  parser.add_argument(
      "--pass_hidden_state", type="bool", nargs="?", const=True,
      default=True,
      help="""\
      Whether to pass encoder's hidden state to decoder when using an attention
      based model.\
      """)

  # optimizer
  parser.add_argument("--optimizer", type=str, default="sgd", help="sgd | adam")
  parser.add_argument("--learning_rate", type=float, default=1.0,
                      help="Learning rate. Adam: 0.001 | 0.0001")
  parser.add_argument("--warmup_steps", type=int, default=0,
                      help="How many steps we inverse-decay learning.")
  parser.add_argument("--warmup_scheme", type=str, default="t2t", help="""\
      How to warmup learning rates. Options include:
        t2t: Tensor2Tensor's way, start with lr 100 times smaller, then
             exponentiate until the specified lr.\
      """)
  parser.add_argument("--start_decay_step", type=int, default=0,
                      help="When we start to decay")
  parser.add_argument("--decay_steps", type=int, default=10000,
                      help="How frequent we decay")
  parser.add_argument("--decay_factor", type=float, default=1.0,
                      help="How much we decay.")
  parser.add_argument(
      "--learning_rate_decay_scheme", type=str, default="", help="""\
      If specified, overwrite start_decay_step, decay_steps, decay_factor.
      Options include:
        luong: after 1/2 num train steps, we start halving the learning rate
        for 5 times before finishing.
        luong10: same as luong but halve the learning rate 10 times instead.\
      """)

  parser.add_argument(
      "--num_train_steps", type=int, default=12000, help="Num steps to train.")
  parser.add_argument("--colocate_gradients_with_ops", type="bool", nargs="?",
                      const=True,
                      default=True,
                      help=("Whether try colocating gradients with "
                            "corresponding op"))

  # initializer
  parser.add_argument("--init_op", type=str, default="uniform",
                      help="uniform | glorot_normal | glorot_uniform")
  parser.add_argument("--init_weight", type=float, default=0.1,
                      help=("for uniform init_op, initialize weights "
                            "between [-this, this]."))

  # data
  #parser.add_argument("--src", type=str, default="en",
                      #help="Source suffix, e.g., en.")
  #parser.add_argument("--tgt", type=str, default="fr",
                      #help="Target suffix, e.g., de.")
  #parser.add_argument("--train_src", type=str, default="/home/ruiwang/Documents/medical letter/newstest2013.en",
  #                    help="Train prefix, expect files with src/tgt suffixes.")
  #parser.add_argument("--train_tgt", type=str, default="/home/ruiwang/Documents/medical letter/newstest2013.fr",
  #                    help="Train prefix, expect files with src/tgt suffixes.")
  
  #parser.add_argument("--dev_src", type=str, default="/home/ruiwang/Documents/medical letter/newssyscomb2009.en",
  #                    help="Dev prefix, expect files with src/tgt suffixes.")  
  #parser.add_argument("--dev_tgt", type=str, default="/home/ruiwang/Documents/medical letter/newssyscomb2009.fr",
  #                    help="Dev prefix, expect files with src/tgt suffixes.")
  
  #parser.add_argument("--test_src", type=str, default="/home/ruiwang/Documents/medical letter/newstest2009.en",
  #                    help="Test prefix, expect files with src/tgt suffixes.")
  #parser.add_argument("--test_tgt", type=str, default="/home/ruiwang/Documents/medical letter/newstest2009.fr",
  #                    help="Test prefix, expect files with src/tgt suffixes.")
  

  #parser.add_argument("--out_hparam", type=str, default="/home/ruiwang/Documents/medical letter/hparam_rui",
  #                    help="")
  
  #parser.add_argument("--best_metric_path", type=str, default="/home/ruiwang/Documents/medical letter/best_metric",
  #                    help="")
  parser.add_argument("--out_model_info", type=str, default="/home/ruiwang/Documents/medical letter/my_nmt_model.txt",
                      help="")
  #parser.add_argument("--log_path", type=str, default="/home/ruiwang/Documents/medical letter/log_rui",
  #                    help="") --out_model_info
  #parser.add_argument("--summary_path", type=str, default="/home/ruiwang/Documents/medical letter/summary_rui",
  #                    help="")
  #parser.add_argument("--ckpt_path", type=str, default="/home/ruiwang/Documents/medical letter/",
  #                    help="")
  
  parser.add_argument("--out_dir", type=str, default="Model_dir",
                      help="Store log/model files.")
  
  #parser.add_argument("--out_model", type=str, default="/home/ruiwang/Documents/medical letter/",
  #                    help="")
  #parser.add_argument("--out_model_index", type=str, default="/home/ruiwang/Documents/medical letter/Model_dir",
   #                   help="")
  #parser.add_argument("--out_model_meta", type=str, default="/home/ruiwang/Documents/medical letter/Model_dir",
   #                   help="")

  # Vocab
  parser.add_argument("--vocab_src", type=str, default="/home/ruiwang/Documents/medical letter/vocab40000.en", help="""\
      Vocab prefix, expect files with src/tgt suffixes.If None, extract from
      train files.\
      """)
  parser.add_argument("--vocab_tgt", type=str, default="/home/ruiwang/Documents/medical letter/vocab40000.fr", help="""\
      Vocab prefix, expect files with src/tgt suffixes.If None, extract from
      train files.\
      """)
  
  
  
  
  
  
  
  
  parser.add_argument("--sos", type=str, default="<s>",
                      help="Start-of-sentence symbol.")
  parser.add_argument("--eos", type=str, default="</s>",
                      help="End-of-sentence symbol.")
  parser.add_argument("--share_vocab", type="bool", nargs="?", const=True,
                      default=False,
                      help="""\
      Whether to use the source vocab and embeddings for both source and
      target.\
      """)
  parser.add_argument("--check_special_token", type="bool", default=True,
                      help="""\
                      Whether check special sos, eos, unk tokens exist in the
                      vocab files.\
                      """)

  # Sequence lengths
  parser.add_argument("--src_max_len", type=int, default=50,
                      help="Max length of src sequences during training.")
  parser.add_argument("--tgt_max_len", type=int, default=50,
                      help="Max length of tgt sequences during training.")
  parser.add_argument("--src_max_len_infer", type=int, default=None,
                      help="Max length of src sequences during inference.")
  parser.add_argument("--tgt_max_len_infer", type=int, default=None,
                      help="""\
      Max length of tgt sequences during inference.  Also use to restrict the
      maximum decoding length.\
      """)

  # Default settings works well (rarely need to change)
  parser.add_argument("--unit_type", type=str, default="lstm",
                      help="lstm | gru | layer_norm_lstm | nas")
  parser.add_argument("--forget_bias", type=float, default=1.0,
                      help="Forget bias for BasicLSTMCell.")
  parser.add_argument("--dropout", type=float, default=0.2,
                      help="Dropout rate (not keep_prob)")
  parser.add_argument("--max_gradient_norm", type=float, default=5.0,
                      help="Clip gradients to this norm.")
  parser.add_argument("--source_reverse", type="bool", nargs="?", const=True,
                      default=False, help="Reverse source sequence.")
  parser.add_argument("--batch_size", type=int, default=128, help="Batch size.")

  parser.add_argument("--steps_per_stats", type=int, default=100,
                      help=("How many training steps to do per stats logging."
                            "Save checkpoint every 10x steps_per_stats"))
  parser.add_argument("--max_train", type=int, default=0,
                      help="Limit on the size of training data (0: no limit).")
  parser.add_argument("--num_buckets", type=int, default=5,
                      help="Put data into similar-length buckets.")

  # SPM
  parser.add_argument("--subword_option", type=str, default="",
                      choices=["", "bpe", "spm"],
                      help="""\
                      Set to bpe or spm to activate subword desegmentation.\
                      """)

  # Misc
  parser.add_argument("--num_gpus", type=int, default=1,
                      help="Number of gpus in each worker.")
  parser.add_argument("--log_device_placement", type="bool", nargs="?",
                      const=True, default=False, help="Debug GPU allocation.")
  parser.add_argument("--metrics", type=str, default="bleu",
                      help=("Comma-separated list of evaluations "
                            "metrics (bleu,rouge,accuracy)"))
  parser.add_argument("--steps_per_external_eval", type=int, default=None,
                      help="""\
      How many training steps to do per external evaluation.  Automatically set
      based on data if None.\
      """)
  parser.add_argument("--scope", type=str, default=None,
                      help="scope to put variables under")
  parser.add_argument("--hparams_path", type=str, default="/home/ruiwang/Documents/medical letter/hparam_rui",
                      help=("Path to standard hparams json file that overrides"
                            "hparams values from FLAGS."))
  parser.add_argument("--random_seed", type=int, default=None,
                      help="Random seed (>0, set a specific seed).")
  parser.add_argument("--override_loaded_hparams", type="bool", nargs="?",
                      const=True, default=False,
                      help="Override loaded hparams with values specified")

  # Inference
  parser.add_argument("--ckpt", type=str, default="",
                      help="Checkpoint file to load a model for inference.")
  parser.add_argument("--inference_input_file", type=str, default="/home/ruiwang/Documents/medical letter/newssyscomb2009.en",
                      help="Set to the text to decode.")
  parser.add_argument("--inference_list", type=str, default=None,
                      help=("A comma-separated list of sentence indices "
                            "(0-based) to decode."))
  parser.add_argument("--infer_batch_size", type=int, default=32,
                      help="Batch size for inference mode.")
  parser.add_argument("--inference_output_file", type=str, default="/home/ruiwang/Documents/medical letter/newssyscomb2009translated.txt",
                      help="Output file to store decoding results.")
  parser.add_argument("--inference_ref_file", type=str, default=None,
                      help=("""\
      Reference file to compute evaluation scores (if provided).\
      """))
  parser.add_argument("--beam_width", type=int, default=0,
                      help=("""\
      beam width when using beam search decoder. If 0 (default), use standard
      decoder with greedy helper.\
      """))
  parser.add_argument("--length_penalty_weight", type=float, default=0.0,
                      help="Length penalty for beam search.")
  parser.add_argument("--num_translations_per_input", type=int, default=1,
                      help=("""\
      Number of translations generated for each sentence. This is only used for
      inference.\
      """))

  # Job info
  parser.add_argument("--jobid", type=int, default=0,
                      help="Task id of the worker.")
  parser.add_argument("--num_workers", type=int, default=1,
                      help="Number of workers (inference only).")


def create_hparams(flags):
  """Create training hparams."""
  return tf.contrib.training.HParams(
      # Data
      #src=flags.src,
      #tgt=flags.tgt,
      #train_src=flags.train_src,
      #train_tgt=flags.train_tgt,
      
      #dev_src=flags.dev_src,
      #dev_tgt=flags.dev_tgt,
      
      #test_src=flags.test_src,
      #test_tgt=flags.test_tgt,
      
      vocab_src=flags.vocab_src,
      vocab_tgt=flags.vocab_tgt,
      
      
      
      out_dir=flags.out_dir,
      #out_hparam = flags.out_hparam,
      #best_metric_path = flags.best_metric_path,
      out_model_info = flags.out_model_info,
      #log_path = flags.log_path,
      #summary_path = flags.summary_path,
      #ckpt_path = flags.ckpt_path,
      
      

      # Networks
      num_units=flags.num_units,
      num_layers=flags.num_layers,
      dropout=flags.dropout,
      unit_type=flags.unit_type,
      encoder_type=flags.encoder_type,
      residual=flags.residual,
      time_major=flags.time_major,
      num_embeddings_partitions=flags.num_embeddings_partitions,

      # Attention mechanisms
      attention=flags.attention,
      attention_architecture=flags.attention_architecture,
      output_attention=flags.output_attention,
      pass_hidden_state=flags.pass_hidden_state,

      # Train
      optimizer=flags.optimizer,
      num_train_steps=flags.num_train_steps,
      batch_size=flags.batch_size,
      init_op=flags.init_op,
      init_weight=flags.init_weight,
      max_gradient_norm=flags.max_gradient_norm,
      learning_rate=flags.learning_rate,
      warmup_steps=flags.warmup_steps,
      warmup_scheme=flags.warmup_scheme,
      start_decay_step=flags.start_decay_step,
      decay_factor=flags.decay_factor,
      decay_steps=flags.decay_steps,
      learning_rate_decay_scheme=flags.learning_rate_decay_scheme,
      colocate_gradients_with_ops=flags.colocate_gradients_with_ops,

      # Data constraints
      num_buckets=flags.num_buckets,
      max_train=flags.max_train,
      src_max_len=flags.src_max_len,
      tgt_max_len=flags.tgt_max_len,
      source_reverse=flags.source_reverse,

      # Inference
      src_max_len_infer=flags.src_max_len_infer,
      tgt_max_len_infer=flags.tgt_max_len_infer,
      infer_batch_size=flags.infer_batch_size,
      beam_width=flags.beam_width,
      length_penalty_weight=flags.length_penalty_weight,
      num_translations_per_input=flags.num_translations_per_input,

      # Vocab
      sos=flags.sos if flags.sos else vocab_utils.SOS,
      eos=flags.eos if flags.eos else vocab_utils.EOS,
      subword_option=flags.subword_option,
      check_special_token=flags.check_special_token,

      # Misc
      forget_bias=flags.forget_bias,
      num_gpus=flags.num_gpus,
      epoch_step=0,  # record where we were within an epoch.
      steps_per_stats=flags.steps_per_stats,
      steps_per_external_eval=flags.steps_per_external_eval,
      share_vocab=flags.share_vocab,
      metrics=flags.metrics.split(","),
      log_device_placement=flags.log_device_placement,
      random_seed=flags.random_seed,
      override_loaded_hparams=flags.override_loaded_hparams,
  )


def ensure_compatible_hparams(hparams, default_hparams, hparams_path):
  """Make sure the loaded hparams is compatible with new changes."""
  #default_hparams = utils.maybe_parse_standard_hparams(
  #    default_hparams, hparams_path)

  # For compatible reason, if there are new fields in default_hparams,
  #   we add them to the current hparams
  default_config = default_hparams.values()
  config = hparams.values()
  for key in default_config:
    if key not in config:
      hparams.add_hparam(key, default_config[key])

  # Update all hparams' keys if override_loaded_hparams=True
  if default_hparams.override_loaded_hparams:
    for key in default_config:
      if getattr(hparams, key) != default_config[key]:
        utils.print_out("# Updating hparams.%s: %s -> %s" %
                        (key, str(getattr(hparams, key)),
                         str(default_config[key])))
        setattr(hparams, key, default_config[key])
  return hparams



def load_hparams_Alveo(
    out_dir, default_hparams, hparams_path, save_hparams=True):
  """Create hparams or load hparams from out_dir."""

  hparams = utils.load_hparams(out_dir)

  hparams = ensure_compatible_hparams(hparams, default_hparams, hparams_path)

  # Print HParams
  if save_hparams:
    utils.save_hparams(out_dir, hparams)
    for metric in hparams.metrics:
      utils.save_hparams(getattr(hparams, "best_" + metric + "_dir"), hparams)
  utils.print_hparams(hparams)
  return hparams




def infer_main(flags, default_hparams, inference_fn, target_session=""):
  """Run main."""
  # Job
  jobid = flags.jobid
  num_workers = flags.num_workers
  utils.print_out("# Job id %d" % jobid)

  # Random
  random_seed = flags.random_seed
  if random_seed is not None and random_seed > 0:
    utils.print_out("# Set random seed to %d" % random_seed)
    random.seed(random_seed + jobid)
    np.random.seed(random_seed + jobid)

  ## Train / Decode
  #root = default_hparams.out_model_info.split('/')
  #parent_path = ''
  #for i in range(len(root)-1):
  #    parent_path += root[i] + '/'
  
  out_model_file = flags.out_model_info
  infile = open ( out_model_file, 'r')
  out_dir = ""
  for line in infile:
      out_dir = line.rstrip( '\r\n' )
      break

  flags.out_dir = out_dir #parent_path + flags.out_dir
  
  default_hparams.out_dir = out_dir

      
  
  hparams = load_hparams_Alveo(out_dir, default_hparams, flags.hparams_path, save_hparams=True)
  #hparams.out_dir = out_dir
  #
  
  print(hparams.num_units)
  print(hparams.dropout)
  print(hparams.attention)
  print(hparams.train_src)
  print(hparams.dev_src)

  
  print(hparams.out_model_info)
  print(hparams.out_dir)

  
  hparams.inference_indices = None
  if flags.inference_list:
    (hparams.inference_indices) = (
        [int(token) for token in flags.inference_list.split(",")])

  # Inference
  trans_file = flags.inference_output_file
  ckpt = flags.ckpt
  if not ckpt:
    ckpt = tf.train.latest_checkpoint(out_dir)
  inference_fn(ckpt, flags.inference_input_file,
               trans_file, hparams, num_workers, jobid)

  # Evaluation
  ref_file = flags.inference_ref_file
  if ref_file and tf.gfile.Exists(trans_file):
    for metric in hparams.metrics:
      score = evaluation_utils.evaluate(
          ref_file,
          trans_file,
          metric,
          hparams.subword_option)
      utils.print_out("  %s: %.1f" % (metric, score))

  #latest_ckpt = tf.train.latest_checkpoint(default_hparams.out_dir)
  
  #print (latest_ckpt)


def main(unused_argv):
  default_hparams = create_hparams(FLAGS)
  print(default_hparams.attention)
  print(default_hparams.num_units)
  #train_fn = train.train
  inference_fn = inference.inference
  infer_main(FLAGS, default_hparams, inference_fn)


if __name__ == "__main__":
  nmt_parser = argparse.ArgumentParser()
  add_arguments(nmt_parser)
  FLAGS, unparsed = nmt_parser.parse_known_args()
  #print("system argvs")
  #print(sys.argv)



  tf.app.run(main=main, argv=[sys.argv] + unparsed)

