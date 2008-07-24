/* ---------------------------------------------------------------------------
 #
 #       L-Py: L-systems in Python
 #
 #       Copyright 2003-2008 UMR Cirad/Inria/Inra Dap - Virtual Plant Team
 #
 #       File author(s): F. Boudon (frederic.boudon@cirad.fr)
 #
 # ---------------------------------------------------------------------------
 #
 #                      GNU General Public Licence
 #
 #       This program is free software; you can redistribute it and/or
 #       modify it under the terms of the GNU General Public License as
 #       published by the Free Software Foundation; either version 2 of
 #       the License, or (at your option) any later version.
 #
 #       This program is distributed in the hope that it will be useful,
 #       but WITHOUT ANY WARRANTY; without even the implied warranty of
 #       MERCHANTABILITY or FITNESS For A PARTICULAR PURPOSE. See the
 #       GNU General Public License for more details.
 #
 #       You should have received a copy of the GNU General Public
 #       License along with this program; see the file COPYING. If not,
 #       write to the Free Software Foundation, Inc., 59
 #       Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 #
 # ---------------------------------------------------------------------------
 */

#include "lsysrule.h"
using namespace boost::python;
#include <string>

PYLSYS_USING_NAMESPACE

AxialTree::const_iterator getPos(const AxialTree& tree, int pos){
  if(pos < 0)pos += tree.size();
  AxialTree::const_iterator beg = tree.begin();
  if(pos > 0 && pos < tree.size())beg += pos;
  else if(pos != 0){
	PyErr_SetString(PyExc_IndexError, "index out of range");
    throw_error_already_set();
  }
  return beg;
}


int match(LsysRule * rule,const AxialTree& tree, int pos, AxialTree& dest) {
  AxialTree::const_iterator beg = getPos(tree,pos);
  AxialTree::const_iterator endpos;
  if(!rule->match(tree,beg,dest,endpos))return -1;
  return tree.pos(endpos);
}

object match2(LsysRule * rule,const AxialTree& tree, int pos ) {
  AxialTree::const_iterator beg = getPos(tree,pos);
  AxialTree::const_iterator endpos;
  AxialTree dest;
  if(!rule->match(tree,beg,dest,endpos))return object(-1);
  return make_tuple(dest,tree.pos(endpos));
}

object match1(LsysRule * rule,const AxialTree& tree) {
    return match2(rule,tree,0);
}

int reverse_match(LsysRule * rule,const AxialTree& tree, int pos, AxialTree& dest) {
  AxialTree::const_iterator beg = getPos(tree,pos);
  AxialTree::const_iterator endpos;
  if(!rule->reverse_match(tree,beg,dest,endpos))return -1;
  return tree.pos(endpos);
}

boost::python::object reverse_match2(LsysRule * rule,const AxialTree& tree, int pos) {
  AxialTree::const_iterator beg = getPos(tree,pos);
  AxialTree::const_iterator endpos;
  AxialTree dest;
  if(!rule->reverse_match(tree,beg,dest,endpos))return object(-1);
  return make_tuple(dest,tree.pos(endpos));
}

boost::python::object reverse_match1(LsysRule * rule,const AxialTree& tree) {
    return reverse_match2(rule,tree,-1);
}

object call(LsysRule * rule) {
  object res = rule->apply();
  if(res == object())return res;
  else return res;
}

object call(LsysRule * rule,const list& args) {
  object res = rule->apply(args);
  if(res == object())return res;
  else return res;
}

object call(LsysRule * rule,const tuple& args) {
  object res = rule->apply(args);
  if(res == object())return res;
  else return res;
}

void Lr_set(LsysRule * rule, const std::string& code) {
  rule->set(code);
  rule->compile();
}

void export_LsysRule(){

  class_<LsysRule>
	("LsysRule", init<optional<size_t,size_t,char> >("LsysRule(id,group,prefix)"))
	.def("__str__", &LsysRule::str)
	//.def("__repr__", &LsysRule::str)
	.def("__call__", (object(*)(LsysRule *) )&call)
	.def("__call__", (object(*)(LsysRule *,const list&) )&call)
	.def("__call__", (object(*)(LsysRule *,const tuple&))&call)
	.add_property("id",&LsysRule::getId,&LsysRule::setId)
	.add_property("id",&LsysRule::getGroupId,&LsysRule::setGroupId)
	.add_property("lineno",make_getter(&LsysRule::lineno))
	.def("predecessor",&LsysRule::predecessor, boost::python::return_internal_reference<1>())
	.def("leftContext", &LsysRule::leftContext, boost::python::return_internal_reference<1>())
	.def("newLeftContext", &LsysRule::newLeftContext, boost::python::return_internal_reference<1>())
	.def("rightContext", &LsysRule::rightContext, boost::python::return_internal_reference<1>())
	.def("newRightContext", &LsysRule::newRightContext, boost::python::return_internal_reference<1>())
	.def("function",   &LsysRule::function, boost::python::return_internal_reference<1>())
	.def("definition", &LsysRule::definition, boost::python::return_internal_reference<1>())
	.def("compiled",&LsysRule::compiled)
	.def("compile",(void(LsysRule::*)())&LsysRule::compile)
	.def("compile",(void(LsysRule::*)(dict&))&LsysRule::compile)
	.def("clear", &LsysRule::clear)
	.def("nbParameters", &LsysRule::nbParameters)
	.def("nbContexts", &LsysRule::nbContexts)
	.def("isContextFree", &LsysRule::isContextFree)
	.def("hasQuery", &LsysRule::hasQuery)
	.def("functionName", &LsysRule::functionName)
	.def("name", &LsysRule::name)
	.def("code", &LsysRule::getCode)
	.def("set", &Lr_set)
	.def("match", &match)
	.def("match", &match2)
	.def("match", &match1)
	.def("reverse_match", &reverse_match)
	.def("reverse_match", &reverse_match2)
	.def("reverse_match", &reverse_match1)
	.def("process", &LsysRule::process)
	.def("forwardCompatible", &LsysRule::forwardCompatible)
	.def("backwardCompatible", &LsysRule::backwardCompatible)
	;
}
