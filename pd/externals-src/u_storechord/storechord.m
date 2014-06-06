/*
 * Joe White (white.joe4@gmail.com) & Dominik Hierner, 2011
 *
 * u_storechord is a midi note handling Pd external. It creates a priority list of held down notes 
 * and selects the right midi message to output. 
 *
 * Useful to stop note off messages being sent to a monophonic synth 
 */

#import <Foundation/Foundation.h>
#include "m_pd.h"
#include <string.h>

static t_class *u_storechord_class;

typedef struct _u_storechord {

  t_object x_obj;
  t_outlet *noteOutletLeft;
  t_outlet *noteOutletRight;
  NSMutableArray *arrayOfNoteOnPitches;
  NSMutableArray *arrayOfNoteOnScaleSteps;
} t_u_storechord;

static void *u_storechord_new(t_symbol *s) {
  
  t_u_storechord *x = (t_u_storechord *)pd_new(u_storechord_class);
  
  inlet_new(&x->x_obj, &x->x_obj.ob_pd, gensym("bang"), gensym("clear"));
  
  x->noteOutletLeft = outlet_new(&x->x_obj, &s_list);
  x->noteOutletRight = outlet_new(&x->x_obj, &s_list);
  x->arrayOfNoteOnPitches = [[NSMutableArray alloc] init];
	x->arrayOfNoteOnScaleSteps = [[NSMutableArray alloc] init];
	
  return (void *)x;
}

static void *u_storechord_free(t_u_storechord *x) {
  
  [x->arrayOfNoteOnPitches release];
  [x->arrayOfNoteOnScaleSteps release];
  x->arrayOfNoteOnPitches = nil;
  x->arrayOfNoteOnScaleSteps = nil;
	x = nil;
  return 0;
}

void u_storechord_output_list(t_u_storechord *x, int outletIndex, t_float scaleStep,
                    t_float midiPitch, t_float midiVelocity) {
 
  t_atom outputAtom[2];
  
  switch (outletIndex) {
    case 0:
      // Outputs to midi device
      SETFLOAT(outputAtom, midiPitch);
      SETFLOAT(outputAtom+1, midiVelocity);
      outlet_list(x->noteOutletLeft, &s_list, 2, outputAtom);
      break;
      
    case 1:
      // Sends to another chord module
      SETFLOAT(outputAtom, scaleStep);
      SETFLOAT(outputAtom+1, midiVelocity);
      outlet_list(x->noteOutletRight, &s_list, 2, outputAtom);
      break;
      
    default:
      post("Error: output index unknown");
      break;
  }
}

void u_storechord_clear_array(t_u_storechord *x) {
  [x->arrayOfNoteOnPitches removeAllObjects];
  [x->arrayOfNoteOnScaleSteps removeAllObjects];
}


static void *u_storechord_note_in(t_u_storechord *x, t_symbol *s, int argc, t_atom *argv) {

  t_float scaleStep;
  t_float midiPitch;
  t_float midiVelocity;
  
  // expecting a list of 3 floats in the following structure: 'scaleStep midiPitch midiVelocity'
  if (argc == 3 && argv->a_type == A_FLOAT
            && (argv+1)->a_type == A_FLOAT
            && (argv+2)->a_type == A_FLOAT) {
    scaleStep = atom_getfloat(argv);
    midiPitch = atom_getfloat(argv+1);
    midiVelocity = atom_getfloat(argv+2);
  } else {
    post("u_storechord: wrong input arguments, 'scalestep pitch velocity' needed.");
    return x;
  }

  NSNumber *step = [NSNumber numberWithFloat:scaleStep];
  NSNumber *pitch = [NSNumber numberWithFloat:midiPitch];
  
  if (![x->arrayOfNoteOnPitches containsObject:pitch]) {
    
    if (midiVelocity > 0) { // add note to set
      [x->arrayOfNoteOnPitches addObject:pitch];
      [x->arrayOfNoteOnScaleSteps addObject:step];
      
      u_storechord_output_list(x, 0, scaleStep, midiPitch, midiVelocity);
      
    } else if (midiVelocity == 0) { // no respective note-on, note-off ignored
      u_storechord_output_list(x, 1, scaleStep, midiPitch, midiVelocity);
    }
    
  } else if ([x->arrayOfNoteOnPitches containsObject:pitch]) {
    if (midiVelocity > 0) { // note being played twice, shouldn't be possible (don  t add to array)
      u_storechord_output_list(x, 0, scaleStep, midiPitch, midiVelocity);
      
    } else if (midiVelocity == 0) {
      if (![x->arrayOfNoteOnScaleSteps containsObject:step]) { // note is not from this chord
        u_storechord_output_list(x, 1, scaleStep, midiPitch, midiVelocity);
      }
      
      if ([x->arrayOfNoteOnScaleSteps containsObject:step]) {
        if ([x->arrayOfNoteOnPitches indexOfObject:pitch]
            == [x->arrayOfNoteOnScaleSteps indexOfObject:step]) { // note off message
          [x->arrayOfNoteOnPitches removeObject:pitch];
          [x->arrayOfNoteOnScaleSteps removeObject:step];
          u_storechord_output_list(x, 0, scaleStep, midiPitch, midiVelocity);
          
        } else {
          // note-off is for a different chord (ignored)
          u_storechord_output_list(x, 1, scaleStep, midiPitch, midiVelocity);
        }
      }
    }  
  }
  return x;
}  
  
void u_storechord_setup(void)
{
  u_storechord_class = class_new(gensym("u_storechord"), 
                               (t_newmethod)u_storechord_new, 
                               (t_method)u_storechord_free,
                               sizeof(t_u_storechord), 0, 0);
  
  class_addmethod(u_storechord_class, (t_method)u_storechord_clear_array, gensym("clear"), 0);
  class_addlist(u_storechord_class, u_storechord_note_in);
}