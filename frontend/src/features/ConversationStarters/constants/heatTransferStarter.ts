import type { TopicStarter } from "../models/starters.types";

export const HEAT_TRANSFER_CONVERSATION_STARTERS: TopicStarter[] = [
  {
    id: "basics_of_heat_transfer",
    title: "Basics of Heat Transfer",
    starters: [
      "Explain conduction, convection, and radiation, and identify the dominant mode in a given system.",
      "Solve a basic heat-transfer problem using an energy balance and clear assumptions.",
      "Generate a short quiz on heat-transfer modes and basic energy balances.",
    ],
  },

  {
    id: "energy_balances",
    title: "Energy Balances",
    starters: [
      "Compare macro, integral, and differential energy balances with one physical example.",
      "Derive a differential energy equation from a microbalance on a differential slice.",
      "Generate a quiz that tests which balance form to use in each scenario.",
    ],
  },

  {
    id: "one_dimensional_conduction",
    title: "1D Conduction (With and Without Heat Generation)",
    starters: [
      "Compare 1D conduction in Cartesian, cylindrical, and spherical coordinates.",
      "Show how internal heat generation changes the 1D conduction equation and solution form.",
      "Solve 1D conduction using both direct differential-equation solution and the integral method.",
    ],
  },

  {
    id: "thermal_resistance",
    title: "Thermal Resistance",
    starters: [
      "Build a thermal-resistance network for Cartesian, cylindrical, and spherical conduction.",
      "Include convection and contact resistances and combine them correctly.",
      "Derive critical (optimal) insulation thickness for cylindrical and spherical systems.",
    ],
  },

  {
    id: "extended_surfaces",
    title: "Extended Surfaces (Fins)",
    starters: [
      "Solve fin problems for common boundary conditions and compare solution forms.",
      "Explain fin effectiveness vs fin efficiency and when each metric matters.",
      "Derive the fin equation and walk through the standard fin solutions.",
    ],
  },

  {
    id: "unsteady_conduction",
    title: "Unsteady Conduction",
    starters: [
      "Derive and interpret the penetration depth scaling: delta ~ sqrt(alpha*t).",
      "Apply Biot-number criteria to choose lumped vs spatially varying models.",
      "Compare early-time methods: error-function (result form) vs integral approximation.",
    ],
  },

  {
    id: "convection",
    title: "Convection Fundamentals",
    starters: [
      "Explain velocity and thermal boundary layers and their link to skin friction and heat transfer.",
      "Relate Nu to h, define Pr, and connect Re, Pr, and Nu physically.",
      "Derive simplified continuity, momentum, and energy equations for steady incompressible flow.",
    ],
  },

  {
    id: "external_forced_convection",
    title: "External Forced Convection",
    starters: [
      "Derive laminar flat-plate scalings: delta/x ~ Re^(-1/2) and delta_t/x ~ Re^(-1/2)Pr^m.",
      "Obtain local and average skin-friction and Nusselt relations for laminar external flow.",
      "Generate a quiz on selecting the correct external-flow convection relation.",
    ],
  },

  {
    id: "internal_forced_convection",
    title: "Internal Forced Convection",
    starters: [
      "Derive/interpret Nu and Cf for fully developed flow in cylindrical ducts.",
      "Distinguish hydrodynamic and thermal development regions in internal flow.",
      "Practice choosing the right internal-flow correlation from flow and thermal conditions.",
    ],
  },

  {
    id: "natural_convection",
    title: "Natural Convection",
    starters: [
      "Derive natural-convection Nu scaling for laminar external flow using Grashof number.",
      "Interpret Gr, Pr, and Nu roles in free-convection heat transfer.",
      "Decide when a problem is natural, forced, or mixed convection.",
    ],
  },

  {
    id: "convection_correlations",
    title: "Convection Correlations & Problem Solving",
    starters: [
      "Use a decision flow to pick correlations by internal/external flow and geometry.",
      "Choose correlations correctly for natural vs forced convection and laminar vs turbulent regimes.",
      "Generate a mixed quiz where I select correlations before solving.",
    ],
  },

  {
    id: "final_exam_review",
    title: "Final Exam Review",
    starters: [
      "Build a focused review plan from my weak topics across heat transfer.",
      "Quiz me across conduction, convection, resistance networks, fins, and transients.",
      "Give me mixed exam-style problems and coach my solution setup step by step.",
      "Test me on assumptions, governing equations, and validity checks (Bi, Re, Pr, Nu, Gr).",
    ],
  },
];
