DEBUG:numba.core.ssa:on stmt: $phi166.1 = $164get_iter.35
DEBUG:numba.core.ssa:on stmt: jump 166
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 166
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE33A0>
DEBUG:numba.core.ssa:on stmt: $166for_iter.2 = iternext(value=$phi166.1)
DEBUG:numba.core.ssa:on stmt: $166for_iter.3 = pair_first(value=$166for_iter.2)
DEBUG:numba.core.ssa:on stmt: $166for_iter.4 = pair_second(value=$166for_iter.2)
DEBUG:numba.core.ssa:on stmt: $phi168.2 = $166for_iter.3
DEBUG:numba.core.ssa:on stmt: branch $166for_iter.4, 168, 236
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 168
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE33A0>
DEBUG:numba.core.ssa:on stmt: i = $phi168.2
DEBUG:numba.core.ssa:on stmt: $178binary_multiply.7 = i * index_step
DEBUG:numba.core.ssa:on stmt: $180binary_add.8 = offset.1 + $178binary_multiply.7
DEBUG:numba.core.ssa:on stmt: $182binary_subscr.9 = getitem(value=interp_win, index=$180binary_add.8, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $194binary_multiply.15 = i * index_step
DEBUG:numba.core.ssa:on stmt: $196binary_add.16 = offset.1 + $194binary_multiply.15       
DEBUG:numba.core.ssa:on stmt: $198binary_subscr.17 = getitem(value=interp_delta, index=$196binary_add.16, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $200binary_multiply.18 = eta * $198binary_subscr.17
DEBUG:numba.core.ssa:on stmt: weight = $182binary_subscr.9 + $200binary_multiply.18       
DEBUG:numba.core.ssa:on stmt: $212binary_subscr.24 = getitem(value=y, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $222binary_subtract.29 = n.1 - i
DEBUG:numba.core.ssa:on stmt: $224binary_subscr.30 = getitem(value=x, index=$222binary_subtract.29, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $226binary_multiply.31 = weight * $224binary_subscr.30
DEBUG:numba.core.ssa:on stmt: $228inplace_add.32 = inplace_binop(fn=<built-in function iadd>, immutable_fn=<built-in function add>, lhs=$212binary_subscr.24, rhs=$226binary_multiply.31, static_lhs=Undefined, static_rhs=Undefined)
DEBUG:numba.core.ssa:on stmt: y[t] = $228inplace_add.32
DEBUG:numba.core.ssa:on stmt: jump 166
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 236
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE33A0>
DEBUG:numba.core.ssa:on stmt: $240binary_subtract.3 = scale - frac.1
DEBUG:numba.core.ssa:on stmt: frac.2 = $240binary_subtract.3
DEBUG:numba.core.ssa:on stmt: index_frac.2 = frac.2 * num_table
DEBUG:numba.core.ssa:on stmt: $252load_global.7 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: offset.2 = call $252load_global.7(index_frac.2, func=$252load_global.7, args=[Var(index_frac.2, interpn.py:64)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: eta = index_frac.2 - offset.2
DEBUG:numba.core.ssa:replaced with: eta.2 = index_frac.2 - offset.2
DEBUG:numba.core.ssa:on stmt: $268load_global.13 = global(min: <built-in function min>)   
DEBUG:numba.core.ssa:on stmt: $274binary_subtract.16 = n_orig - n.1
DEBUG:numba.core.ssa:on stmt: $const276.17 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $278binary_subtract.18 = $274binary_subtract.16 - $const276.17
DEBUG:numba.core.ssa:on stmt: $284binary_subtract.21 = nwin - offset.2
DEBUG:numba.core.ssa:on stmt: $288binary_floor_divide.23 = $284binary_subtract.21 // index_step
DEBUG:numba.core.ssa:on stmt: k_max = call $268load_global.13($278binary_subtract.18, $288binary_floor_divide.23, func=$268load_global.13, args=[Var($278binary_subtract.18, interpn.py:71), Var($288binary_floor_divide.23, interpn.py:71)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $294load_global.25 = global(range: <class 'range'>)
DEBUG:numba.core.ssa:on stmt: $298call_function.27 = call $294load_global.25(k_max, func=$294load_global.25, args=[Var(k_max, interpn.py:71)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $300get_iter.28 = getiter(value=$298call_function.27)       
DEBUG:numba.core.ssa:on stmt: $phi302.1 = $300get_iter.28
DEBUG:numba.core.ssa:on stmt: jump 302
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 302
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE33A0>
DEBUG:numba.core.ssa:on stmt: $302for_iter.2 = iternext(value=$phi302.1)
DEBUG:numba.core.ssa:on stmt: $302for_iter.3 = pair_first(value=$302for_iter.2)
DEBUG:numba.core.ssa:on stmt: $302for_iter.4 = pair_second(value=$302for_iter.2)
DEBUG:numba.core.ssa:on stmt: $phi304.2 = $302for_iter.3
DEBUG:numba.core.ssa:on stmt: branch $302for_iter.4, 304, 376
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 304
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE33A0>
DEBUG:numba.core.ssa:on stmt: k = $phi304.2
DEBUG:numba.core.ssa:on stmt: $314binary_multiply.7 = k * index_step
DEBUG:numba.core.ssa:on stmt: $316binary_add.8 = offset.2 + $314binary_multiply.7
DEBUG:numba.core.ssa:on stmt: $318binary_subscr.9 = getitem(value=interp_win, index=$316binary_add.8, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $330binary_multiply.15 = k * index_step
DEBUG:numba.core.ssa:on stmt: $332binary_add.16 = offset.2 + $330binary_multiply.15       
DEBUG:numba.core.ssa:on stmt: $334binary_subscr.17 = getitem(value=interp_delta, index=$332binary_add.16, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $336binary_multiply.18 = eta * $334binary_subscr.17
DEBUG:numba.core.ssa:on stmt: weight = $318binary_subscr.9 + $336binary_multiply.18       
DEBUG:numba.core.ssa:on stmt: $348binary_subscr.24 = getitem(value=y, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $358binary_add.29 = n.1 + k
DEBUG:numba.core.ssa:on stmt: $const360.30 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $362binary_add.31 = $358binary_add.29 + $const360.30        
DEBUG:numba.core.ssa:on stmt: $364binary_subscr.32 = getitem(value=x, index=$362binary_add.31, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $366binary_multiply.33 = weight * $364binary_subscr.32      
DEBUG:numba.core.ssa:on stmt: $368inplace_add.34 = inplace_binop(fn=<built-in function iadd>, immutable_fn=<built-in function add>, lhs=$348binary_subscr.24, rhs=$366binary_multiply.33, static_lhs=Undefined, static_rhs=Undefined)
DEBUG:numba.core.ssa:on stmt: y[t] = $368inplace_add.34
DEBUG:numba.core.ssa:on stmt: jump 302
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 376
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE33A0>
DEBUG:numba.core.ssa:on stmt: jump 80
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 378
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE33A0>
DEBUG:numba.core.ssa:on stmt: $const378.0 = const(NoneType, None)
DEBUG:numba.core.ssa:on stmt: $380return_value.1 = cast(value=$const378.0)
DEBUG:numba.core.ssa:on stmt: return $380return_value.1
DEBUG:numba.core.ssa:Replaced assignments: defaultdict(<class 'list'>,
            {0: [<numba.core.ir.Assign object at 0x000001E1C7EE0F10>],
             82: [<numba.core.ir.Assign object at 0x000001E1C7EE28C0>],
             236: [<numba.core.ir.Assign object at 0x000001E1C7EE3910>]})
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 0
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: x = arg(0, name=x)
DEBUG:numba.core.ssa:on stmt: t_out = arg(1, name=t_out)
DEBUG:numba.core.ssa:on stmt: interp_win = arg(2, name=interp_win)
DEBUG:numba.core.ssa:on stmt: interp_delta = arg(3, name=interp_delta)
DEBUG:numba.core.ssa:on stmt: num_table = arg(4, name=num_table)
DEBUG:numba.core.ssa:on stmt: scale = arg(5, name=scale)
DEBUG:numba.core.ssa:on stmt: y = arg(6, name=y)
DEBUG:numba.core.ssa:on stmt: $2load_global.0 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: $8binary_multiply.3 = scale * num_table
DEBUG:numba.core.ssa:on stmt: index_step = call $2load_global.0($8binary_multiply.3, func=$2load_global.0, args=[Var($8binary_multiply.3, interpn.py:20)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: time_register = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: n = const(int, 0)
DEBUG:numba.core.ssa:on stmt: frac = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: index_frac = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: offset = const(int, 0)
DEBUG:numba.core.ssa:on stmt: eta = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: weight = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: $44load_attr.13 = getattr(value=interp_win, attr=shape)     
DEBUG:numba.core.ssa:on stmt: $const46.14 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: nwin = static_getitem(value=$44load_attr.13, index=0, index_var=$const46.14, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $54load_attr.17 = getattr(value=x, attr=shape)
DEBUG:numba.core.ssa:on stmt: $const56.18 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: n_orig = static_getitem(value=$54load_attr.17, index=0, index_var=$const56.18, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $64load_attr.21 = getattr(value=t_out, attr=shape)
DEBUG:numba.core.ssa:on stmt: $const66.22 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: n_out = static_getitem(value=$64load_attr.21, index=0, index_var=$const66.22, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $72load_global.24 = global(prange: <class 'numba.misc.special.prange'>)
DEBUG:numba.core.ssa:on stmt: $76call_function.26 = call $72load_global.24(n_out, func=$72load_global.24, args=[Var(n_out, interpn.py:32)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $78get_iter.27 = getiter(value=$76call_function.26)
DEBUG:numba.core.ssa:on stmt: $phi80.0 = $78get_iter.27
DEBUG:numba.core.ssa:on stmt: jump 80
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 80
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: $80for_iter.1 = iternext(value=$phi80.0)
DEBUG:numba.core.ssa:on stmt: $80for_iter.2 = pair_first(value=$80for_iter.1)
DEBUG:numba.core.ssa:on stmt: $80for_iter.3 = pair_second(value=$80for_iter.1)
DEBUG:numba.core.ssa:on stmt: $phi82.1 = $80for_iter.2
DEBUG:numba.core.ssa:on stmt: branch $80for_iter.3, 82, 378
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 82
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: t = $phi82.1
DEBUG:numba.core.ssa:on stmt: time_register.1 = getitem(value=t_out, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $92load_global.5 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: n.1 = call $92load_global.5(time_register.1, func=$92load_global.5, args=[Var(time_register.1, interpn.py:35)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $106binary_subtract.11 = time_register.1 - n.1
DEBUG:numba.core.ssa:on stmt: frac.1 = scale * $106binary_subtract.11
DEBUG:numba.core.ssa:on stmt: index_frac.1 = frac.1 * num_table
DEBUG:numba.core.ssa:on stmt: $120load_global.16 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: offset.1 = call $120load_global.16(index_frac.1, func=$120load_global.16, args=[Var(index_frac.1, interpn.py:44)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: eta.1 = index_frac.1 - offset.1
DEBUG:numba.core.ssa:on stmt: $136load_global.22 = global(min: <built-in function min>)   
DEBUG:numba.core.ssa:on stmt: $const140.24 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $142binary_add.25 = n.1 + $const140.24
DEBUG:numba.core.ssa:on stmt: $148binary_subtract.28 = nwin - offset.1
DEBUG:numba.core.ssa:on stmt: $152binary_floor_divide.30 = $148binary_subtract.28 // index_step
DEBUG:numba.core.ssa:on stmt: i_max = call $136load_global.22($142binary_add.25, $152binary_floor_divide.30, func=$136load_global.22, args=[Var($142binary_add.25, interpn.py:51), Var($152binary_floor_divide.30, interpn.py:51)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $158load_global.32 = global(range: <class 'range'>)
DEBUG:numba.core.ssa:on stmt: $162call_function.34 = call $158load_global.32(i_max, func=$158load_global.32, args=[Var(i_max, interpn.py:51)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $164get_iter.35 = getiter(value=$162call_function.34)       
DEBUG:numba.core.ssa:on stmt: $phi166.1 = $164get_iter.35
DEBUG:numba.core.ssa:on stmt: jump 166
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 166
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: $166for_iter.2 = iternext(value=$phi166.1)
DEBUG:numba.core.ssa:on stmt: $166for_iter.3 = pair_first(value=$166for_iter.2)
DEBUG:numba.core.ssa:on stmt: $166for_iter.4 = pair_second(value=$166for_iter.2)
DEBUG:numba.core.ssa:on stmt: $phi168.2 = $166for_iter.3
DEBUG:numba.core.ssa:on stmt: branch $166for_iter.4, 168, 236
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 168
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: i = $phi168.2
DEBUG:numba.core.ssa:on stmt: $178binary_multiply.7 = i * index_step
DEBUG:numba.core.ssa:on stmt: $180binary_add.8 = offset.1 + $178binary_multiply.7
DEBUG:numba.core.ssa:on stmt: $182binary_subscr.9 = getitem(value=interp_win, index=$180binary_add.8, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $194binary_multiply.15 = i * index_step
DEBUG:numba.core.ssa:on stmt: $196binary_add.16 = offset.1 + $194binary_multiply.15       
DEBUG:numba.core.ssa:on stmt: $198binary_subscr.17 = getitem(value=interp_delta, index=$196binary_add.16, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $200binary_multiply.18 = eta * $198binary_subscr.17
DEBUG:numba.core.ssa:find_def var='eta' stmt=$200binary_multiply.18 = eta * $198binary_subscr.17
DEBUG:numba.core.ssa:find_def_from_top label 168
DEBUG:numba.core.ssa:idom 166 from label 168
DEBUG:numba.core.ssa:find_def_from_bottom label 166
DEBUG:numba.core.ssa:find_def_from_top label 166
DEBUG:numba.core.ssa:idom 82 from label 166
DEBUG:numba.core.ssa:find_def_from_bottom label 82
DEBUG:numba.core.ssa:replaced with: $200binary_multiply.18 = eta.1 * $198binary_subscr.17 
DEBUG:numba.core.ssa:on stmt: weight = $182binary_subscr.9 + $200binary_multiply.18       
DEBUG:numba.core.ssa:on stmt: $212binary_subscr.24 = getitem(value=y, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $222binary_subtract.29 = n.1 - i
DEBUG:numba.core.ssa:on stmt: $224binary_subscr.30 = getitem(value=x, index=$222binary_subtract.29, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $226binary_multiply.31 = weight * $224binary_subscr.30      
DEBUG:numba.core.ssa:on stmt: $228inplace_add.32 = inplace_binop(fn=<built-in function iadd>, immutable_fn=<built-in function add>, lhs=$212binary_subscr.24, rhs=$226binary_multiply.31, static_lhs=Undefined, static_rhs=Undefined)
DEBUG:numba.core.ssa:on stmt: y[t] = $228inplace_add.32
DEBUG:numba.core.ssa:on stmt: jump 166
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 236
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: $240binary_subtract.3 = scale - frac.1
DEBUG:numba.core.ssa:on stmt: frac.2 = $240binary_subtract.3
DEBUG:numba.core.ssa:on stmt: index_frac.2 = frac.2 * num_table
DEBUG:numba.core.ssa:on stmt: $252load_global.7 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: offset.2 = call $252load_global.7(index_frac.2, func=$252load_global.7, args=[Var(index_frac.2, interpn.py:64)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: eta.2 = index_frac.2 - offset.2
DEBUG:numba.core.ssa:on stmt: $268load_global.13 = global(min: <built-in function min>)   
DEBUG:numba.core.ssa:on stmt: $274binary_subtract.16 = n_orig - n.1
DEBUG:numba.core.ssa:on stmt: $const276.17 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $278binary_subtract.18 = $274binary_subtract.16 - $const276.17
DEBUG:numba.core.ssa:on stmt: $284binary_subtract.21 = nwin - offset.2
DEBUG:numba.core.ssa:on stmt: $288binary_floor_divide.23 = $284binary_subtract.21 // index_step
DEBUG:numba.core.ssa:on stmt: k_max = call $268load_global.13($278binary_subtract.18, $288binary_floor_divide.23, func=$268load_global.13, args=[Var($278binary_subtract.18, interpn.py:71), Var($288binary_floor_divide.23, interpn.py:71)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $294load_global.25 = global(range: <class 'range'>)
DEBUG:numba.core.ssa:on stmt: $298call_function.27 = call $294load_global.25(k_max, func=$294load_global.25, args=[Var(k_max, interpn.py:71)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $300get_iter.28 = getiter(value=$298call_function.27)       
DEBUG:numba.core.ssa:on stmt: $phi302.1 = $300get_iter.28
DEBUG:numba.core.ssa:on stmt: jump 302
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 302
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: $302for_iter.2 = iternext(value=$phi302.1)
DEBUG:numba.core.ssa:on stmt: $302for_iter.3 = pair_first(value=$302for_iter.2)
DEBUG:numba.core.ssa:on stmt: $302for_iter.4 = pair_second(value=$302for_iter.2)
DEBUG:numba.core.ssa:on stmt: $phi304.2 = $302for_iter.3
DEBUG:numba.core.ssa:on stmt: branch $302for_iter.4, 304, 376
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 304
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: k = $phi304.2
DEBUG:numba.core.ssa:on stmt: $314binary_multiply.7 = k * index_step
DEBUG:numba.core.ssa:on stmt: $316binary_add.8 = offset.2 + $314binary_multiply.7
DEBUG:numba.core.ssa:on stmt: $318binary_subscr.9 = getitem(value=interp_win, index=$316binary_add.8, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $330binary_multiply.15 = k * index_step
DEBUG:numba.core.ssa:on stmt: $332binary_add.16 = offset.2 + $330binary_multiply.15       
DEBUG:numba.core.ssa:on stmt: $334binary_subscr.17 = getitem(value=interp_delta, index=$332binary_add.16, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $336binary_multiply.18 = eta * $334binary_subscr.17
DEBUG:numba.core.ssa:find_def var='eta' stmt=$336binary_multiply.18 = eta * $334binary_subscr.17
DEBUG:numba.core.ssa:find_def_from_top label 304
DEBUG:numba.core.ssa:idom 302 from label 304
DEBUG:numba.core.ssa:find_def_from_bottom label 302
DEBUG:numba.core.ssa:find_def_from_top label 302
DEBUG:numba.core.ssa:idom 236 from label 302
DEBUG:numba.core.ssa:find_def_from_bottom label 236
DEBUG:numba.core.ssa:replaced with: $336binary_multiply.18 = eta.2 * $334binary_subscr.17 
DEBUG:numba.core.ssa:on stmt: weight = $318binary_subscr.9 + $336binary_multiply.18       
DEBUG:numba.core.ssa:on stmt: $348binary_subscr.24 = getitem(value=y, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $358binary_add.29 = n.1 + k
DEBUG:numba.core.ssa:on stmt: $const360.30 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $362binary_add.31 = $358binary_add.29 + $const360.30        
DEBUG:numba.core.ssa:on stmt: $364binary_subscr.32 = getitem(value=x, index=$362binary_add.31, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $366binary_multiply.33 = weight * $364binary_subscr.32      
DEBUG:numba.core.ssa:on stmt: $368inplace_add.34 = inplace_binop(fn=<built-in function iadd>, immutable_fn=<built-in function add>, lhs=$348binary_subscr.24, rhs=$366binary_multiply.33, static_lhs=Undefined, static_rhs=Undefined)
DEBUG:numba.core.ssa:on stmt: y[t] = $368inplace_add.34
DEBUG:numba.core.ssa:on stmt: jump 302
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 376
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: jump 80
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 378
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE3F40>    
DEBUG:numba.core.ssa:on stmt: $const378.0 = const(NoneType, None)
DEBUG:numba.core.ssa:on stmt: $380return_value.1 = cast(value=$const378.0)
DEBUG:numba.core.ssa:on stmt: return $380return_value.1
DEBUG:numba.core.ssa:Fix SSA violator on var weight
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 0
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: x = arg(0, name=x)
DEBUG:numba.core.ssa:on stmt: t_out = arg(1, name=t_out)
DEBUG:numba.core.ssa:on stmt: interp_win = arg(2, name=interp_win)
DEBUG:numba.core.ssa:on stmt: interp_delta = arg(3, name=interp_delta)
DEBUG:numba.core.ssa:on stmt: num_table = arg(4, name=num_table)
DEBUG:numba.core.ssa:on stmt: scale = arg(5, name=scale)
DEBUG:numba.core.ssa:on stmt: y = arg(6, name=y)
DEBUG:numba.core.ssa:on stmt: $2load_global.0 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: $8binary_multiply.3 = scale * num_table
DEBUG:numba.core.ssa:on stmt: index_step = call $2load_global.0($8binary_multiply.3, func=$2load_global.0, args=[Var($8binary_multiply.3, interpn.py:20)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: time_register = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: n = const(int, 0)
DEBUG:numba.core.ssa:on stmt: frac = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: index_frac = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: offset = const(int, 0)
DEBUG:numba.core.ssa:on stmt: eta = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: weight = const(float, 0.0)
DEBUG:numba.core.ssa:first assign: weight
DEBUG:numba.core.ssa:replaced with: weight = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: $44load_attr.13 = getattr(value=interp_win, attr=shape)     
DEBUG:numba.core.ssa:on stmt: $const46.14 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: nwin = static_getitem(value=$44load_attr.13, index=0, index_var=$const46.14, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $54load_attr.17 = getattr(value=x, attr=shape)
DEBUG:numba.core.ssa:on stmt: $const56.18 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: n_orig = static_getitem(value=$54load_attr.17, index=0, index_var=$const56.18, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $64load_attr.21 = getattr(value=t_out, attr=shape)
DEBUG:numba.core.ssa:on stmt: $const66.22 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: n_out = static_getitem(value=$64load_attr.21, index=0, index_var=$const66.22, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $72load_global.24 = global(prange: <class 'numba.misc.special.prange'>)
DEBUG:numba.core.ssa:on stmt: $76call_function.26 = call $72load_global.24(n_out, func=$72load_global.24, args=[Var(n_out, interpn.py:32)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $78get_iter.27 = getiter(value=$76call_function.26)
DEBUG:numba.core.ssa:on stmt: $phi80.0 = $78get_iter.27
DEBUG:numba.core.ssa:on stmt: jump 80
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 80
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: $80for_iter.1 = iternext(value=$phi80.0)
DEBUG:numba.core.ssa:on stmt: $80for_iter.2 = pair_first(value=$80for_iter.1)
DEBUG:numba.core.ssa:on stmt: $80for_iter.3 = pair_second(value=$80for_iter.1)
DEBUG:numba.core.ssa:on stmt: $phi82.1 = $80for_iter.2
DEBUG:numba.core.ssa:on stmt: branch $80for_iter.3, 82, 378
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 82
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: t = $phi82.1
DEBUG:numba.core.ssa:on stmt: time_register.1 = getitem(value=t_out, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $92load_global.5 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: n.1 = call $92load_global.5(time_register.1, func=$92load_global.5, args=[Var(time_register.1, interpn.py:35)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $106binary_subtract.11 = time_register.1 - n.1
DEBUG:numba.core.ssa:on stmt: frac.1 = scale * $106binary_subtract.11
DEBUG:numba.core.ssa:on stmt: index_frac.1 = frac.1 * num_table
DEBUG:numba.core.ssa:on stmt: $120load_global.16 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: offset.1 = call $120load_global.16(index_frac.1, func=$120load_global.16, args=[Var(index_frac.1, interpn.py:44)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: eta.1 = index_frac.1 - offset.1
DEBUG:numba.core.ssa:on stmt: $136load_global.22 = global(min: <built-in function min>)   
DEBUG:numba.core.ssa:on stmt: $const140.24 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $142binary_add.25 = n.1 + $const140.24
DEBUG:numba.core.ssa:on stmt: $148binary_subtract.28 = nwin - offset.1
DEBUG:numba.core.ssa:on stmt: $152binary_floor_divide.30 = $148binary_subtract.28 // index_step
DEBUG:numba.core.ssa:on stmt: i_max = call $136load_global.22($142binary_add.25, $152binary_floor_divide.30, func=$136load_global.22, args=[Var($142binary_add.25, interpn.py:51), Var($152binary_floor_divide.30, interpn.py:51)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $158load_global.32 = global(range: <class 'range'>)
DEBUG:numba.core.ssa:on stmt: $162call_function.34 = call $158load_global.32(i_max, func=$158load_global.32, args=[Var(i_max, interpn.py:51)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $164get_iter.35 = getiter(value=$162call_function.34)       
DEBUG:numba.core.ssa:on stmt: $phi166.1 = $164get_iter.35
DEBUG:numba.core.ssa:on stmt: jump 166
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 166
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: $166for_iter.2 = iternext(value=$phi166.1)
DEBUG:numba.core.ssa:on stmt: $166for_iter.3 = pair_first(value=$166for_iter.2)
DEBUG:numba.core.ssa:on stmt: $166for_iter.4 = pair_second(value=$166for_iter.2)
DEBUG:numba.core.ssa:on stmt: $phi168.2 = $166for_iter.3
DEBUG:numba.core.ssa:on stmt: branch $166for_iter.4, 168, 236
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 168
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: i = $phi168.2
DEBUG:numba.core.ssa:on stmt: $178binary_multiply.7 = i * index_step
DEBUG:numba.core.ssa:on stmt: $180binary_add.8 = offset.1 + $178binary_multiply.7
DEBUG:numba.core.ssa:on stmt: $182binary_subscr.9 = getitem(value=interp_win, index=$180binary_add.8, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $194binary_multiply.15 = i * index_step
DEBUG:numba.core.ssa:on stmt: $196binary_add.16 = offset.1 + $194binary_multiply.15       
DEBUG:numba.core.ssa:on stmt: $198binary_subscr.17 = getitem(value=interp_delta, index=$196binary_add.16, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $200binary_multiply.18 = eta.1 * $198binary_subscr.17       
DEBUG:numba.core.ssa:on stmt: weight = $182binary_subscr.9 + $200binary_multiply.18       
DEBUG:numba.core.ssa:replaced with: weight.1 = $182binary_subscr.9 + $200binary_multiply.18
DEBUG:numba.core.ssa:on stmt: $212binary_subscr.24 = getitem(value=y, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $222binary_subtract.29 = n.1 - i
DEBUG:numba.core.ssa:on stmt: $224binary_subscr.30 = getitem(value=x, index=$222binary_subtract.29, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $226binary_multiply.31 = weight * $224binary_subscr.30      
DEBUG:numba.core.ssa:on stmt: $228inplace_add.32 = inplace_binop(fn=<built-in function iadd>, immutable_fn=<built-in function add>, lhs=$212binary_subscr.24, rhs=$226binary_multiply.31, static_lhs=Undefined, static_rhs=Undefined)
DEBUG:numba.core.ssa:on stmt: y[t] = $228inplace_add.32
DEBUG:numba.core.ssa:on stmt: jump 166
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 236
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: $240binary_subtract.3 = scale - frac.1
DEBUG:numba.core.ssa:on stmt: frac.2 = $240binary_subtract.3
DEBUG:numba.core.ssa:on stmt: index_frac.2 = frac.2 * num_table
DEBUG:numba.core.ssa:on stmt: $252load_global.7 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: offset.2 = call $252load_global.7(index_frac.2, func=$252load_global.7, args=[Var(index_frac.2, interpn.py:64)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: eta.2 = index_frac.2 - offset.2
DEBUG:numba.core.ssa:on stmt: $268load_global.13 = global(min: <built-in function min>)   
DEBUG:numba.core.ssa:on stmt: $274binary_subtract.16 = n_orig - n.1
DEBUG:numba.core.ssa:on stmt: $const276.17 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $278binary_subtract.18 = $274binary_subtract.16 - $const276.17
DEBUG:numba.core.ssa:on stmt: $284binary_subtract.21 = nwin - offset.2
DEBUG:numba.core.ssa:on stmt: $288binary_floor_divide.23 = $284binary_subtract.21 // index_step
DEBUG:numba.core.ssa:on stmt: k_max = call $268load_global.13($278binary_subtract.18, $288binary_floor_divide.23, func=$268load_global.13, args=[Var($278binary_subtract.18, interpn.py:71), Var($288binary_floor_divide.23, interpn.py:71)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $294load_global.25 = global(range: <class 'range'>)
DEBUG:numba.core.ssa:on stmt: $298call_function.27 = call $294load_global.25(k_max, func=$294load_global.25, args=[Var(k_max, interpn.py:71)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $300get_iter.28 = getiter(value=$298call_function.27)       
DEBUG:numba.core.ssa:on stmt: $phi302.1 = $300get_iter.28
DEBUG:numba.core.ssa:on stmt: jump 302
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 302
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: $302for_iter.2 = iternext(value=$phi302.1)
DEBUG:numba.core.ssa:on stmt: $302for_iter.3 = pair_first(value=$302for_iter.2)
DEBUG:numba.core.ssa:on stmt: $302for_iter.4 = pair_second(value=$302for_iter.2)
DEBUG:numba.core.ssa:on stmt: $phi304.2 = $302for_iter.3
DEBUG:numba.core.ssa:on stmt: branch $302for_iter.4, 304, 376
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 304
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: k = $phi304.2
DEBUG:numba.core.ssa:on stmt: $314binary_multiply.7 = k * index_step
DEBUG:numba.core.ssa:on stmt: $316binary_add.8 = offset.2 + $314binary_multiply.7
DEBUG:numba.core.ssa:on stmt: $318binary_subscr.9 = getitem(value=interp_win, index=$316binary_add.8, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $330binary_multiply.15 = k * index_step
DEBUG:numba.core.ssa:on stmt: $332binary_add.16 = offset.2 + $330binary_multiply.15       
DEBUG:numba.core.ssa:on stmt: $334binary_subscr.17 = getitem(value=interp_delta, index=$332binary_add.16, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $336binary_multiply.18 = eta.2 * $334binary_subscr.17       
DEBUG:numba.core.ssa:on stmt: weight = $318binary_subscr.9 + $336binary_multiply.18       
DEBUG:numba.core.ssa:replaced with: weight.2 = $318binary_subscr.9 + $336binary_multiply.18
DEBUG:numba.core.ssa:on stmt: $348binary_subscr.24 = getitem(value=y, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $358binary_add.29 = n.1 + k
DEBUG:numba.core.ssa:on stmt: $const360.30 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $362binary_add.31 = $358binary_add.29 + $const360.30        
DEBUG:numba.core.ssa:on stmt: $364binary_subscr.32 = getitem(value=x, index=$362binary_add.31, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $366binary_multiply.33 = weight * $364binary_subscr.32      
DEBUG:numba.core.ssa:on stmt: $368inplace_add.34 = inplace_binop(fn=<built-in function iadd>, immutable_fn=<built-in function add>, lhs=$348binary_subscr.24, rhs=$366binary_multiply.33, static_lhs=Undefined, static_rhs=Undefined)
DEBUG:numba.core.ssa:on stmt: y[t] = $368inplace_add.34
DEBUG:numba.core.ssa:on stmt: jump 302
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 376
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: jump 80
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 378
DEBUG:numba.core.ssa:Running <numba.core.ssa._FreshVarHandler object at 0x000001E1C7EE3D90>
DEBUG:numba.core.ssa:on stmt: $const378.0 = const(NoneType, None)
DEBUG:numba.core.ssa:on stmt: $380return_value.1 = cast(value=$const378.0)
DEBUG:numba.core.ssa:on stmt: return $380return_value.1
DEBUG:numba.core.ssa:Replaced assignments: defaultdict(<class 'list'>,
            {0: [<numba.core.ir.Assign object at 0x000001E1C7EE1D20>],
             168: [<numba.core.ir.Assign object at 0x000001E1C7EE33D0>],
             304: [<numba.core.ir.Assign object at 0x000001E1C7DB7700>]})
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 0
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: x = arg(0, name=x)
DEBUG:numba.core.ssa:on stmt: t_out = arg(1, name=t_out)
DEBUG:numba.core.ssa:on stmt: interp_win = arg(2, name=interp_win)
DEBUG:numba.core.ssa:on stmt: interp_delta = arg(3, name=interp_delta)
DEBUG:numba.core.ssa:on stmt: num_table = arg(4, name=num_table)
DEBUG:numba.core.ssa:on stmt: scale = arg(5, name=scale)
DEBUG:numba.core.ssa:on stmt: y = arg(6, name=y)
DEBUG:numba.core.ssa:on stmt: $2load_global.0 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: $8binary_multiply.3 = scale * num_table
DEBUG:numba.core.ssa:on stmt: index_step = call $2load_global.0($8binary_multiply.3, func=$2load_global.0, args=[Var($8binary_multiply.3, interpn.py:20)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: time_register = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: n = const(int, 0)
DEBUG:numba.core.ssa:on stmt: frac = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: index_frac = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: offset = const(int, 0)
DEBUG:numba.core.ssa:on stmt: eta = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: weight = const(float, 0.0)
DEBUG:numba.core.ssa:on stmt: $44load_attr.13 = getattr(value=interp_win, attr=shape)     
DEBUG:numba.core.ssa:on stmt: $const46.14 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: nwin = static_getitem(value=$44load_attr.13, index=0, index_var=$const46.14, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $54load_attr.17 = getattr(value=x, attr=shape)
DEBUG:numba.core.ssa:on stmt: $const56.18 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: n_orig = static_getitem(value=$54load_attr.17, index=0, index_var=$const56.18, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $64load_attr.21 = getattr(value=t_out, attr=shape)
DEBUG:numba.core.ssa:on stmt: $const66.22 = const(int, 0)
DEBUG:numba.core.ssa:on stmt: n_out = static_getitem(value=$64load_attr.21, index=0, index_var=$const66.22, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $72load_global.24 = global(prange: <class 'numba.misc.special.prange'>)
DEBUG:numba.core.ssa:on stmt: $76call_function.26 = call $72load_global.24(n_out, func=$72load_global.24, args=[Var(n_out, interpn.py:32)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $78get_iter.27 = getiter(value=$76call_function.26)
DEBUG:numba.core.ssa:on stmt: $phi80.0 = $78get_iter.27
DEBUG:numba.core.ssa:on stmt: jump 80
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 80
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: $80for_iter.1 = iternext(value=$phi80.0)
DEBUG:numba.core.ssa:on stmt: $80for_iter.2 = pair_first(value=$80for_iter.1)
DEBUG:numba.core.ssa:on stmt: $80for_iter.3 = pair_second(value=$80for_iter.1)
DEBUG:numba.core.ssa:on stmt: $phi82.1 = $80for_iter.2
DEBUG:numba.core.ssa:on stmt: branch $80for_iter.3, 82, 378
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 82
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: t = $phi82.1
DEBUG:numba.core.ssa:on stmt: time_register.1 = getitem(value=t_out, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $92load_global.5 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: n.1 = call $92load_global.5(time_register.1, func=$92load_global.5, args=[Var(time_register.1, interpn.py:35)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $106binary_subtract.11 = time_register.1 - n.1
DEBUG:numba.core.ssa:on stmt: frac.1 = scale * $106binary_subtract.11
DEBUG:numba.core.ssa:on stmt: index_frac.1 = frac.1 * num_table
DEBUG:numba.core.ssa:on stmt: $120load_global.16 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: offset.1 = call $120load_global.16(index_frac.1, func=$120load_global.16, args=[Var(index_frac.1, interpn.py:44)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: eta.1 = index_frac.1 - offset.1
DEBUG:numba.core.ssa:on stmt: $136load_global.22 = global(min: <built-in function min>)   
DEBUG:numba.core.ssa:on stmt: $const140.24 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $142binary_add.25 = n.1 + $const140.24
DEBUG:numba.core.ssa:on stmt: $148binary_subtract.28 = nwin - offset.1
DEBUG:numba.core.ssa:on stmt: $152binary_floor_divide.30 = $148binary_subtract.28 // index_step
DEBUG:numba.core.ssa:on stmt: i_max = call $136load_global.22($142binary_add.25, $152binary_floor_divide.30, func=$136load_global.22, args=[Var($142binary_add.25, interpn.py:51), Var($152binary_floor_divide.30, interpn.py:51)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $158load_global.32 = global(range: <class 'range'>)
DEBUG:numba.core.ssa:on stmt: $162call_function.34 = call $158load_global.32(i_max, func=$158load_global.32, args=[Var(i_max, interpn.py:51)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $164get_iter.35 = getiter(value=$162call_function.34)       
DEBUG:numba.core.ssa:on stmt: $phi166.1 = $164get_iter.35
DEBUG:numba.core.ssa:on stmt: jump 166
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 166
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: $166for_iter.2 = iternext(value=$phi166.1)
DEBUG:numba.core.ssa:on stmt: $166for_iter.3 = pair_first(value=$166for_iter.2)
DEBUG:numba.core.ssa:on stmt: $166for_iter.4 = pair_second(value=$166for_iter.2)
DEBUG:numba.core.ssa:on stmt: $phi168.2 = $166for_iter.3
DEBUG:numba.core.ssa:on stmt: branch $166for_iter.4, 168, 236
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 168
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: i = $phi168.2
DEBUG:numba.core.ssa:on stmt: $178binary_multiply.7 = i * index_step
DEBUG:numba.core.ssa:on stmt: $180binary_add.8 = offset.1 + $178binary_multiply.7
DEBUG:numba.core.ssa:on stmt: $182binary_subscr.9 = getitem(value=interp_win, index=$180binary_add.8, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $194binary_multiply.15 = i * index_step
DEBUG:numba.core.ssa:on stmt: $196binary_add.16 = offset.1 + $194binary_multiply.15       
DEBUG:numba.core.ssa:on stmt: $198binary_subscr.17 = getitem(value=interp_delta, index=$196binary_add.16, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $200binary_multiply.18 = eta.1 * $198binary_subscr.17       
DEBUG:numba.core.ssa:on stmt: weight.1 = $182binary_subscr.9 + $200binary_multiply.18     
DEBUG:numba.core.ssa:on stmt: $212binary_subscr.24 = getitem(value=y, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $222binary_subtract.29 = n.1 - i
DEBUG:numba.core.ssa:on stmt: $224binary_subscr.30 = getitem(value=x, index=$222binary_subtract.29, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $226binary_multiply.31 = weight * $224binary_subscr.30      
DEBUG:numba.core.ssa:find_def var='weight' stmt=$226binary_multiply.31 = weight * $224binary_subscr.30
DEBUG:numba.core.ssa:replaced with: $226binary_multiply.31 = weight.1 * $224binary_subscr.30
DEBUG:numba.core.ssa:on stmt: $228inplace_add.32 = inplace_binop(fn=<built-in function iadd>, immutable_fn=<built-in function add>, lhs=$212binary_subscr.24, rhs=$226binary_multiply.31, static_lhs=Undefined, static_rhs=Undefined)
DEBUG:numba.core.ssa:on stmt: y[t] = $228inplace_add.32
DEBUG:numba.core.ssa:on stmt: jump 166
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 236
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: $240binary_subtract.3 = scale - frac.1
DEBUG:numba.core.ssa:on stmt: frac.2 = $240binary_subtract.3
DEBUG:numba.core.ssa:on stmt: index_frac.2 = frac.2 * num_table
DEBUG:numba.core.ssa:on stmt: $252load_global.7 = global(int: <class 'int'>)
DEBUG:numba.core.ssa:on stmt: offset.2 = call $252load_global.7(index_frac.2, func=$252load_global.7, args=[Var(index_frac.2, interpn.py:64)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: eta.2 = index_frac.2 - offset.2
DEBUG:numba.core.ssa:on stmt: $268load_global.13 = global(min: <built-in function min>)   
DEBUG:numba.core.ssa:on stmt: $274binary_subtract.16 = n_orig - n.1
DEBUG:numba.core.ssa:on stmt: $const276.17 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $278binary_subtract.18 = $274binary_subtract.16 - $const276.17
DEBUG:numba.core.ssa:on stmt: $284binary_subtract.21 = nwin - offset.2
DEBUG:numba.core.ssa:on stmt: $288binary_floor_divide.23 = $284binary_subtract.21 // index_step
DEBUG:numba.core.ssa:on stmt: k_max = call $268load_global.13($278binary_subtract.18, $288binary_floor_divide.23, func=$268load_global.13, args=[Var($278binary_subtract.18, interpn.py:71), Var($288binary_floor_divide.23, interpn.py:71)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $294load_global.25 = global(range: <class 'range'>)
DEBUG:numba.core.ssa:on stmt: $298call_function.27 = call $294load_global.25(k_max, func=$294load_global.25, args=[Var(k_max, interpn.py:71)], kws=(), vararg=None, varkwarg=None, target=None)
DEBUG:numba.core.ssa:on stmt: $300get_iter.28 = getiter(value=$298call_function.27)       
DEBUG:numba.core.ssa:on stmt: $phi302.1 = $300get_iter.28
DEBUG:numba.core.ssa:on stmt: jump 302
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 302
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: $302for_iter.2 = iternext(value=$phi302.1)
DEBUG:numba.core.ssa:on stmt: $302for_iter.3 = pair_first(value=$302for_iter.2)
DEBUG:numba.core.ssa:on stmt: $302for_iter.4 = pair_second(value=$302for_iter.2)
DEBUG:numba.core.ssa:on stmt: $phi304.2 = $302for_iter.3
DEBUG:numba.core.ssa:on stmt: branch $302for_iter.4, 304, 376
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 304
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: k = $phi304.2
DEBUG:numba.core.ssa:on stmt: $314binary_multiply.7 = k * index_step
DEBUG:numba.core.ssa:on stmt: $316binary_add.8 = offset.2 + $314binary_multiply.7
DEBUG:numba.core.ssa:on stmt: $318binary_subscr.9 = getitem(value=interp_win, index=$316binary_add.8, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $330binary_multiply.15 = k * index_step
DEBUG:numba.core.ssa:on stmt: $332binary_add.16 = offset.2 + $330binary_multiply.15       
DEBUG:numba.core.ssa:on stmt: $334binary_subscr.17 = getitem(value=interp_delta, index=$332binary_add.16, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $336binary_multiply.18 = eta.2 * $334binary_subscr.17       
DEBUG:numba.core.ssa:on stmt: weight.2 = $318binary_subscr.9 + $336binary_multiply.18     
DEBUG:numba.core.ssa:on stmt: $348binary_subscr.24 = getitem(value=y, index=t, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $358binary_add.29 = n.1 + k
DEBUG:numba.core.ssa:on stmt: $const360.30 = const(int, 1)
DEBUG:numba.core.ssa:on stmt: $362binary_add.31 = $358binary_add.29 + $const360.30        
DEBUG:numba.core.ssa:on stmt: $364binary_subscr.32 = getitem(value=x, index=$362binary_add.31, fn=<built-in function getitem>)
DEBUG:numba.core.ssa:on stmt: $366binary_multiply.33 = weight * $364binary_subscr.32      
DEBUG:numba.core.ssa:find_def var='weight' stmt=$366binary_multiply.33 = weight * $364binary_subscr.32
DEBUG:numba.core.ssa:replaced with: $366binary_multiply.33 = weight.2 * $364binary_subscr.32
DEBUG:numba.core.ssa:on stmt: $368inplace_add.34 = inplace_binop(fn=<built-in function iadd>, immutable_fn=<built-in function add>, lhs=$348binary_subscr.24, rhs=$366binary_multiply.33, static_lhs=Undefined, static_rhs=Undefined)
DEBUG:numba.core.ssa:on stmt: y[t] = $368inplace_add.34
DEBUG:numba.core.ssa:on stmt: jump 302
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 376
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: jump 80
DEBUG:numba.core.ssa:==== SSA block rewrite pass on 378
DEBUG:numba.core.ssa:Running <numba.core.ssa._FixSSAVars object at 0x000001E1C7EE33A0>    
DEBUG:numba.core.ssa:on stmt: $const378.0 = const(NoneType, None)
DEBUG:numba.core.ssa:on stmt: $380return_value.1 = cast(value=$const378.0)
DEBUG:numba.core.ssa:on stmt: return $380return_value.1
Traceback (most recent call last):
  File "D:\Code\voice\ai\rvc\infer\modules\train\train.py", line 639, in <module>
    torch.multiprocessing.set_start_method("spawn")
  File "C:\Users\XGame\AppData\Local\Programs\Python\Python310\lib\multiprocessing\context.py", line 247, in set_start_method
    raise RuntimeError('context has already been set')
RuntimeError: context has already been set
# AI Models

Thư mục này chứa các mô hình AI thay đổi giọng nói như OpenVoice và RVC.

## Cấu trúc
- `openvoice/` - Chứa mô hình OpenVoice đã được clone
- `rvc/` - Chứa mô hình RVC (Retrieval-based Voice Conversion)

## Lưu ý
- Các mô hình AI được tải về và đặt trong thư mục tương ứng
- Không tạo giải pháp dự phòng khi mô hình không hoạt động 