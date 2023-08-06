  # def formatter(self, value):
    #     return "%s%s%s", (self.fmt, value, self.term.normal)
    def _build_hline(self, is_header=False):
        """Return a string used to separated rows or separate header from
        rows
        """
        horiz = self._char_horiz
        if (is_header):
            horiz = self._char_header
        # compute cell separator
        s = "%s%s%s" % (horiz, [horiz, self._char_corner][self._has_vlines()],
            horiz)
        # build the line
        l = s.join([horiz * n for n in self._width])
        # l += horiz if self._deco % 2 == 0 else ""
        l = self.border_formatter(l)
        # add border if needed
        if self._has_border():
            l = "%s%s%s%s%s\n" % (self.border_formatter(self._char_corner), self.border_formatter(horiz), l, self.border_formatter(horiz),
                self.border_formatter(self._char_corner))
        else:
            l += "\n"
        return l
    def _draw_line(self, line, isheader=False):
        """Draw a line

        Loop over a single cell length, over all the cells
        """
        border_formatter = self.border_formatter
        _col_flag = False if len(self.column_formatter) == 0 else True
        _header_flag = False if self.header_formatter is None else True
        if isheader:
            if _header_flag:
                cell_formatter = self.header_formatter
            else:
                if _col_flag:
                    pass
                else:
                    cell_formatter = self.cell_formatter
        else:
            if not _col_flag:
                cell_formatter = self.cell_formatter
            else:
                pass

        line = self._splitit(line, isheader)
        space = " "
        out = ""
        for i in range(len(line[0])):
            if self._has_border():
                if isheader and _header_flag:
                    out += "%s" % border_formatter(self._char_vert)
                    # out += "%s%s" % (border_formatter(self._char_vert), cell_formatter(space))
                else:
                    if _col_flag:
                        out += "%s" % border_formatter(self._char_vert)
                    else:
                        out += "%s%s" % (border_formatter(self._char_vert), cell_formatter(space))
            length = 0
            j = 0
            for cell, width, align in zip(line, self._width, self._align):
                length += 1
                
                # Columnwise style
                if isheader and _header_flag:
                    out += "%s" % cell_formatter(space if self._deco % 2 == 1 else "") if j == 0 else ""
                else:
                    if _col_flag:
                        cell_formatter = self.column_formatter[j]
                        out += "%s" % cell_formatter(space) if j == 0 else ""

                
                cell_line = cell[i]
                fill = width - len(cell_line)
                if isheader:
                    align = self._header_align[length - 1]
                if align == "r":
                    out += cell_formatter(fill * space + cell_line)
                elif align == "c":
                    out += cell_formatter((int(fill/2) * space + cell_line \
                            + int(fill/2 + fill%2) * space))
                else:
                    out += cell_formatter(cell_line + fill * space)
                if length < len(line):
                    space_ = " "
                    if _col_flag:
                        if j >= 0 and not isheader:    
                            space_ = self.column_formatter[j+1](space)
                        else:
                            if not _header_flag:
                                space_ = self.column_formatter[j+1](space)
                            else:
                                space_ = cell_formatter(space)
                    out += "%s%s%s" % (cell_formatter(space),
                                       [cell_formatter(space), border_formatter(self._char_vert)][self._has_vlines()], 
                                       space_)
                j += 1
            out += "%s\n" % ['', cell_formatter(space) + border_formatter(self._char_vert)][self._has_border()]
        return out
    def draw(self):
        """Draw the table

        - the table is returned as a whole string
        """
        _error = "%s%s%s%s%s" % (self.term.red, "Number of attributes in each row should be equal to number of column formatters.", self.term.purple_on_green, " If you are not sure, set the column_format parameter to None", self.term.normal)
        if len(self.column_formatter) != 0:
            assert len(self._rows[0]) == len(self.column_formatter), _error

        if not self._header and not self._rows:
            return
        self._compute_cols_width()
        self._check_align()
        out = ""
        if self._has_border():
            out += self._hline()
        if self._header:
            out += self._draw_line(self._header, isheader=True)
            if self._has_header():
                out += self._hline_header()
        length = 0
        for row in self._rows:
            length += 1
            out += self._draw_line(row)
            if self._has_hlines() and length < len(self._rows):
                out += self._hline()
        if self._has_border():
            out += self._hline()
        return out[:-1]
    
