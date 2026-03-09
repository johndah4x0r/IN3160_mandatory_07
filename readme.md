# Diagrams and implementation
IN3160/4160
Version 2025-01

In this exercise, you will create diagrams, testbench and VHDL code for a pulse density module. 

The key goal for this exercise is to get practice in creating diagrams and understanding their limitations and use in digital design. 
Creating VHDL and testbench is a secondary objective. 
Making a functional pulse density module may help in the next assignment, where the pulse density module can be used as a component or with slight modifications.  

This exercise is also intended to aid understanding of control systems, relevant for the study program in robotics and intelligent systems. 

> [!NOTE]
> Read both the theory and the task description before starting the task.

[Pulse density modulation](pulse-density.md)

[Task description](task.md)

## Delivery checklist

> [!IMPORTANT]
> In this exercise, you shall deliver diagrams according to the task description.
> Diagrams shall be drawn in a capable digital tool[^1], and shall be uploaded together as a single pdf file.
> 
> The python and VHDL code in task d) and e) can be delivered as two separate (.py and .vhd) files or together as a single .zip file.
>
> **Delivery requirements:**
> *  A pdf containing
>    *  the diagrams as specified in a)- c)
>    *  waveform from simulation of d) and e)
> *  Testbench code as specified in d)*
>    *  The testbench should compile and run (past reset and then some…).
>       *  A good test will help you make sure your code can be used later.
> *  VHDL code as implemented in e)*
>    *  The code should compile and be synthesizable
>    *  The code should correspond to the ASM diagram from task c). 
>    *  Having the VHDL pass all tests is not required in this assignment.
>       *  Assignment 8 can be solved without this code, _getting this right will make it easier_.
>       * If your code does not work as intended:
>         * _Make comments and ask two questions for the supervisors_
>           (traversing all your code should not be necessary to aid you)

Functioning PDM modules can be reused in assignment 8, which requires functional PWM (either ordinary PWM or PDM see text below).  

[^1]: We recommend using https://www.drawio.com or https://app.diagrams.net  
  These are online/download versions of the same tool that will be used during the course exam.  

## Supervision guide 
(for lab supervisors)

> [!NOTE]
> **Generally:**
> * Diagrams that correspond to the task.
> * Code that compiles. 
> * If code does not work as specified, try to answer the two questions asked by the students.
> * **Templates are not considered a delivery = hard fail.**
> 
> **Specifically**
> * Datapath diagram
>   * Should correspond to the code in a).
>     * Comment if there are parts that are unclear.
>   * Block diagram
>     * Should match the description in the task.
>       * Comment if there are minor mismatches.
>     * ASM diagram
>       * Does the diagram comply with ASM rules?
>         * This is a requirement to pass. Comment if it does not.
>       * Does the diagram implement pdm according to the task specification?
>         * This is a requirement to pass. Comment if it does not.
>         * If yes, comment if there are easy ways to simplify the implementation or diagram.
>   * Testbench and VHDL module
>     * Does the waveform look reasonable?
>       * If not make a brief comment on what is missing
>     * Stimuli or functionality?
>       * Comment on questions asked.
>       * Check that the code is handed in.
>
> _Getting the ASM diagram right is the main requirement for this task._
> 
> Getting code right is required in assignment 8, not here.
> * _Being set on the right path to be able to solve the next assignment is the main goal for commenting code._
> * Do not spend excessive time commenting code in this task.
> * Comments can be provided orally for students that are able to present their work/ and questions in lab.
> * Please note “oral feedback is given” in canvas when doing so, to make it possible to make sure no one gets forgotten.

