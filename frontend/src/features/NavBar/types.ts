import type { ValidRole } from "../../services";

export type Base = {
  label: string;
  to: string;
  requiresAuth?: boolean
  allowedRoles?: ValidRole[]
};

export type BaseRoute = Base & {
  type: "route";
  items?: Base[];
};

export type DropDownNavRoute = Base & {
  type: "dropdown";
  items: Base[];
};

export type NavigationItem = BaseRoute | DropDownNavRoute;