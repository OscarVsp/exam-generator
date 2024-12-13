# Moore's law

What would you change to make this a fonctionning RISC-V superscalar full-pipeline multi-core processor ?

You only have 69 lines

```vhdl
library ieee;
use ieee.std_logic_1164.ALL;

entity myEntity is Port (
	d_in : in std_logic;
	d_out : in std_logic
); end myEntity;

architecture arch of myEntity is

begin     

	d_in <= d_out;
	 
end arch;
```

![test image](image.jpg)
