%{lua:

function source_macros(file)
  local macro = nil

  for line in io.lines(file) do
    if not macro and line:match("^%%") then
      macro = line:match("^%%(.*)$")
      line = nil
    end

    if macro then
      if line and macro:match("^.-%s*\\%s*$") then
        macro = macro .. '\n' .. line
      end

      if not macro:match("^.-%s*\\%s*$") then
        rpm.define(macro)
        macro = nil
      end
    end
  end
end

}

# Include the constants defined in macros files. Could be dropped as soon as
# RPM supports the %%load macro (RPM 4.12+ probably).
# http://lists.rpm.org/pipermail/rpm-maint/2014-February/003659.html
%define load() %{lua:source_macros(rpm.expand("%1"))}
