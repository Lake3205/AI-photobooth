
export const SCHOOL_TYPES = [
  "praktijk", "basis", "kader", "vmbo", "havo", 
  "vwo", "gymnasium", "mbo", "hbo", "wo"
] as const;

export const GENERATION_TYPES = [
  "Stille generatie", "Boomer", "Verloren generatie", 
  "Patatgeneratie", "Millenial", "Gen Z", "Gen alpha"
] as const;

export const CITIZEN_STATES = [
  "Getrouwd", "Samenwonend", "Single"
] as const;

export type School = typeof SCHOOL_TYPES[number];
export type Generation = typeof GENERATION_TYPES[number];
export type CitizenState = typeof CITIZEN_STATES[number];

export interface AssumptionsProps {
  readonly TheftRate: number;
  readonly School: School;
  readonly Salary: number;
  readonly Generation: Generation;
  readonly Weight: number;
  readonly CitizenState: CitizenState;
  readonly Dept: number;
  readonly FitnessAge: number;
  readonly ScreenTime: number;
}

const VALIDATION_RULES = {
  TheftRate: { min: 1, max: 100 },
  Salary: { min: 0 },
  Weight: { min: 0, max: 1000 },
  Dept: { min: 0 },
  FitnessAge: { min: 0, max: 150 },
  ScreenTime: { min: 0, max: 24 }
} as const;

export class Assumptions implements AssumptionsProps {
  constructor(private readonly props: AssumptionsProps) {
    this.validateProps(props);
  }

  get TheftRate(): number { return this.props.TheftRate; }
  get School(): School { return this.props.School; }
  get Salary(): number { return this.props.Salary; }
  get Generation(): Generation { return this.props.Generation; }
  get Weight(): number { return this.props.Weight; }
  get CitizenState(): CitizenState { return this.props.CitizenState; }
  get Dept(): number { return this.props.Dept; }
  get FitnessAge(): number { return this.props.FitnessAge; }
  get ScreenTime(): number { return this.props.ScreenTime; }

  private validateProps(props: AssumptionsProps): void {
    const errors: string[] = [];


    Object.entries(VALIDATION_RULES).forEach(([key, rules]) => {
      const value = props[key as keyof AssumptionsProps] as number;
      if (value < rules.min || (rules.max && value > rules.max)) {
        errors.push(`${key} must be between ${rules.min} and ${rules.max || 'infinity'}`);
      }
    });


    if (!SCHOOL_TYPES.includes(props.School)) {
      errors.push(`School must be one of: ${SCHOOL_TYPES.join(', ')}`);
    }
    if (!GENERATION_TYPES.includes(props.Generation)) {
      errors.push(`Generation must be one of: ${GENERATION_TYPES.join(', ')}`);
    }
    if (!CITIZEN_STATES.includes(props.CitizenState)) {
      errors.push(`CitizenState must be one of: ${CITIZEN_STATES.join(', ')}`);
    }

    if (errors.length > 0) {
      throw new Error(`Validation failed: ${errors.join('; ')}`);
    }
  }


  public update(updates: Partial<AssumptionsProps>): Assumptions {
    return new Assumptions({ ...this.props, ...updates });
  }


  public toObject(): AssumptionsProps {
    return { ...this.props };
  }
}

export function isValidAssumptions(assumptions: AssumptionsProps): boolean {
  try {
    new Assumptions(assumptions);
    return true;
  } catch {
    return false;
  }
}


