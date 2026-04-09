# Task 7 - Historical anchor copied unchanged from v1 Task 6

Use this task as a direct continuity check only. Do not include it in the default v2 composite average.

Task prompt:

```text
You are reviewing a colleague's Python snippet that checks the bending resistance of a steel beam to EC3. The beam is a 254x102x28 UB, simply supported, carrying a uniform gravity load. Review the code below. Identify any errors - in the engineering logic, units, or use of section properties - correct them, and state clearly whether the section is adequate.
Show your working for the corrected result. If you rely on any section property values, state where they come from.

  # EC3 bending resistance check - 254x102x28 UB
  # Simply supported beam, uniform gravity load

  # Loading
  L = 6.2        # m
  w = 18.5       # kN/m

  M_Ed = (w * L**2) / 8   # kN.m

  # Section properties (254x102x28 UB, Class 1)
  Wpl_z = 49.0e3   # mm^3   <- plastic modulus about z-z axis
  fy    = 275      # N/mm^2
  gamma_M0 = 1.0

  # Resistance (EC3 Cl. 6.2.5)
  M_Rd = (Wpl_z * fy) / gamma_M0   # kN.m

  # Utilisation
  util = M_Ed / M_Rd

  print(f"M_Ed  = {M_Ed:.2f} kN.m")
  print(f"M_Rd  = {M_Rd:.2f} kN.m")
  print(f"Util  = {util:.4f}")
  print("STATUS:", "PASS" if M_Ed <= M_Rd else "FAIL")
```
